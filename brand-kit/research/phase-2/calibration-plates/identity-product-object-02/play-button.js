const vertexShaderSource = `#version 300 es
  in vec2 a_position;
  void main() {
    gl_Position = vec4(a_position, 0.0, 1.0);
  }
`;

const fragmentShaderSource = `#version 300 es
  precision highp float;

  uniform vec2 u_resolution;
  uniform float u_time;
  uniform float u_energy;
  uniform sampler2D u_gradient;
  uniform float u_has_texture;

  out vec4 outColor;

  // Small, branch-free 2D simplex noise. Multiple low-frequency octaves drive
  // the coordinate field, creating liquid deformation rather than rotation.
  vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
  vec3 permute(vec3 x) { return mod289(((x * 34.0) + 10.0) * x); }

  float simplexNoise(vec2 v) {
    const vec4 C = vec4(
      0.211324865405187,
      0.366025403784439,
      -0.577350269189626,
      0.024390243902439
    );

    vec2 i = floor(v + dot(v, C.yy));
    vec2 x0 = v - i + dot(i, C.xx);
    vec2 i1 = x0.x > x0.y ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;
    i = mod289(i);
    vec3 p = permute(
      permute(i.y + vec3(0.0, i1.y, 1.0)) + i.x + vec3(0.0, i1.x, 1.0)
    );
    vec3 m = max(0.5 - vec3(
      dot(x0, x0),
      dot(x12.xy, x12.xy),
      dot(x12.zw, x12.zw)
    ), 0.0);
    m *= m;
    m *= m;
    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;
    m *= 1.79284291400159 - 0.85373472095314 * (a0 * a0 + h * h);
    vec3 g;
    g.x = a0.x * x0.x + h.x * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;
    return 130.0 * dot(m, g);
  }

  float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.52;
    mat2 drift = mat2(0.80, -0.60, 0.60, 0.80);
    for (int octave = 0; octave < 4; octave++) {
      value += amplitude * simplexNoise(p);
      p = drift * p * 2.03 + 7.13;
      amplitude *= 0.48;
    }
    return value;
  }

  float softBlob(vec2 p, vec2 center, float radius) {
    float d = length(p - center);
    return exp(-pow(d / radius, 2.25));
  }

  // Stable screen-space grain: tactile enough to read at rest without creating
  // distracting temporal shimmer during animation.
  float grain(vec2 pixel) {
    vec2 cell = floor(pixel * 0.72);
    return fract(52.9829189 * fract(dot(cell, vec2(0.06711056, 0.00583715))));
  }

  void main() {
    vec2 uv = gl_FragCoord.xy / u_resolution;
    vec2 p = (gl_FragCoord.xy * 2.0 - u_resolution) / min(u_resolution.x, u_resolution.y);
    float t = u_time;

    // Two independently evolving fields fold the mesh in different directions.
    // The long, incommensurate periods keep the movement from reading as a loop.
    vec2 flow = vec2(
      fbm(p * 1.14 + vec2(t * 0.075, -t * 0.043)),
      fbm(p.yx * 1.06 + vec2(-t * 0.052, t * 0.063) + 13.7)
    );
    vec2 folded = p + flow * 0.34;
    folded += 0.09 * vec2(
      sin(folded.y * 2.4 + t * 0.31),
      cos(folded.x * 2.1 - t * 0.27)
    );

    vec3 color;

    if (u_has_texture > 0.5) {
      // Preserve the supplied artwork and animate only its coordinates. Mirrored
      // repeat prevents seams as the liquid field pulls beyond the texture edge.
      vec2 textureFlow = vec2(
        fbm(p * 1.30 + vec2(t * 0.052, -t * 0.031) + 4.2),
        fbm(p.yx * 1.24 + vec2(-t * 0.038, t * 0.047) + 21.3)
      );
      vec2 warpedUv = uv + textureFlow * 0.055;
      warpedUv += 0.012 * vec2(
        sin((uv.y + textureFlow.y) * 8.0 + t * 0.22),
        cos((uv.x + textureFlow.x) * 7.0 - t * 0.19)
      );
      warpedUv = 1.0 - abs(mod(warpedUv, 2.0) - 1.0);
      color = texture(u_gradient, warpedUv).rgb;
    } else {

      vec3 violet = vec3(0.380, 0.255, 0.840);
      vec3 electricBlue = vec3(0.230, 0.655, 1.000);
      vec3 magenta = vec3(0.980, 0.350, 0.825);
      vec3 coral = vec3(1.000, 0.580, 0.500);
      vec3 peach = vec3(1.000, 0.770, 0.675);

      vec2 blueCenter = vec2(
        0.38 + 0.18 * sin(t * 0.21),
        -0.12 + 0.22 * cos(t * 0.17)
      );
      vec2 magentaCenter = vec2(
        0.12 + 0.25 * cos(t * 0.14 + 0.6),
        0.54 + 0.10 * sin(t * 0.23)
      );
      vec2 coralCenter = vec2(
        -0.48 + 0.16 * sin(t * 0.18 + 1.4),
        -0.22 + 0.25 * cos(t * 0.13)
      );

      float blueWeight = pow(softBlob(folded, blueCenter, 0.58), 1.42);
      float magentaWeight = pow(softBlob(folded, magentaCenter, 0.62), 1.38);
      float coralWeight = pow(softBlob(folded, coralCenter, 0.57), 1.42);
      float peachWeight = pow(softBlob(folded, coralCenter + vec2(-0.22, -0.10), 0.31), 1.32);

      // Weighted pigment mixing remains as a no-texture fallback.
      float total = 0.35 + blueWeight * 0.92 + magentaWeight * 1.08 + coralWeight * 1.13 + peachWeight * 0.82;
      color = violet * 0.35;
      color += electricBlue * blueWeight * 0.88;
      color += magenta * magentaWeight * 1.08;
      color += coral * coralWeight * 1.12;
      color += peach * peachWeight * 0.78;
      color /= total;

      float luminance = dot(color, vec3(0.2126, 0.7152, 0.0722));
      color = mix(vec3(luminance), color, 1.16) * 1.055;
    }

    float cloud = fbm(folded * 2.15 - vec2(t * 0.035, t * 0.022));
    float cloudStrength = mix(0.075, 0.028, u_has_texture);
    color *= 0.99 + cloud * cloudStrength;
    color = mix(color, color * 1.12, u_energy);

    float paper = grain(gl_FragCoord.xy) - 0.5;
    float fineGrain = grain(gl_FragCoord.yx * 1.91 + 47.0) - 0.5;
    float paperStrength = mix(0.105, 0.032, u_has_texture);
    float fineStrength = mix(0.045, 0.014, u_has_texture);
    color += paper * paperStrength + fineGrain * fineStrength;

    // A quiet inner vignette helps the circle retain physical volume.
    float edge = smoothstep(0.55, 1.10, length(p));
    color *= 1.015 - edge * 0.105;
    color = pow(max(color, 0.0), vec3(mix(0.88, 0.97, u_has_texture)));

    outColor = vec4(color, 1.0);
  }
`;

const template = document.createElement("template");

template.innerHTML = `
  <style>
    :host {
      --aurora-size: min(300px, calc(100vw - 48px));
      display: inline-grid;
      width: var(--aurora-size);
      height: var(--aurora-size);
      contain: layout paint style;
      isolation: isolate;
    }

    .aurora-button {
      position: relative;
      display: grid;
      width: 100%;
      height: 100%;
      padding: 0;
      overflow: hidden;
      place-items: center;
      appearance: none;
      background: #5d42d7;
      border: 0;
      border-radius: 50%;
      box-shadow: 0 8px 18px rgb(13 13 13 / 7%);
      cursor: pointer;
      outline: none;
      transform: translateZ(0) scale(1);
      transform-origin: center;
      transition:
        transform 430ms cubic-bezier(0.16, 1, 0.3, 1),
        box-shadow 430ms cubic-bezier(0.16, 1, 0.3, 1),
        filter 430ms cubic-bezier(0.16, 1, 0.3, 1);
      -webkit-tap-highlight-color: transparent;
      touch-action: manipulation;
    }

    canvas {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      border-radius: inherit;
      transform: translateZ(0) scale(1.015);
    }

    .wings {
      position: relative;
      z-index: 2;
      display: block;
      width: 50%;
      height: auto;
      color: #f8f8f8;
      filter: drop-shadow(0 2px 3px rgb(31 20 72 / 16%));
      pointer-events: none;
      transform: translate3d(0, calc(var(--aurora-size) * -0.02), 0);
    }

    .aurora-button:active {
      box-shadow: 0 4px 10px rgb(13 13 13 / 8%);
      transform: translateZ(0) scale(0.975);
      transition-duration: 90ms;
    }

    .aurora-button:focus-visible {
      box-shadow:
        0 0 0 4px #f4f2ef,
        0 0 0 7px #17151c,
        0 18px 44px rgb(62 38 140 / 17%);
    }

    .fallback {
      background-image: var(--aurora-image,
        radial-gradient(circle at 72% 62%, #59bdff 0 10%, transparent 42%),
        radial-gradient(circle at 36% 71%, #ff8978 0 13%, transparent 44%),
        radial-gradient(circle at 62% 20%, #ef50d7 0 12%, transparent 48%));
      background-color: #5639c4;
      background-position: center;
      background-size: cover;
    }

    @media (prefers-reduced-motion: reduce) {
      .aurora-button {
        transition-duration: 0.01ms;
      }

      .aurora-button:hover,
      .aurora-button:active {
        transform: none;
      }
    }
  </style>

  <button class="aurora-button" type="button">
    <canvas aria-hidden="true"></canvas>
    <svg
      class="wings"
      viewBox="9 16 340 241"
      role="presentation"
      aria-hidden="true"
    >
      <path fill="currentColor" d="M9.31894 227.388C9.31894 243.442 22.3337 256.457 38.3883 256.457H141.746C157.801 256.457 170.815 243.442 170.815 227.388V172.807C170.815 168.476 169.848 164.201 167.984 160.292L107.284 33.0283C102.46 22.9142 92.2519 16.4734 81.0462 16.4734H38.3883C22.3337 16.4734 9.31894 29.4882 9.31894 45.5427V227.388Z" />
      <path fill="currentColor" d="M348.462 227.388C348.462 243.442 335.447 256.457 319.392 256.457H216.034C199.98 256.457 186.965 243.442 186.965 227.388V172.807C186.965 168.476 187.932 164.201 189.797 160.292L250.497 33.0283C255.321 22.9142 265.529 16.4734 276.734 16.4734H319.392C335.447 16.4734 348.462 29.4882 348.462 45.5427V227.388Z" />
    </svg>
  </button>
`;

function compileShader(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const message = gl.getShaderInfoLog(shader);
    gl.deleteShader(shader);
    throw new Error(`Aurora shader compilation failed: ${message}`);
  }

  return shader;
}

function createProgram(gl) {
  const program = gl.createProgram();
  const vertexShader = compileShader(gl, gl.VERTEX_SHADER, vertexShaderSource);
  const fragmentShader = compileShader(gl, gl.FRAGMENT_SHADER, fragmentShaderSource);

  gl.attachShader(program, vertexShader);
  gl.attachShader(program, fragmentShader);
  gl.linkProgram(program);
  gl.deleteShader(vertexShader);
  gl.deleteShader(fragmentShader);

  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const message = gl.getProgramInfoLog(program);
    gl.deleteProgram(program);
    throw new Error(`Aurora shader linking failed: ${message}`);
  }

  return program;
}

class AuroraPlayButton extends HTMLElement {
  static observedAttributes = ["gradient", "gradient-id", "label", "size"];

  constructor() {
    super();
    this.attachShadow({ mode: "open" }).append(template.content.cloneNode(true));

    this.button = this.shadowRoot.querySelector("button");
    this.canvas = this.shadowRoot.querySelector("canvas");
    this.gl = null;
    this.program = null;
    this.texture = null;
    this.loadedGradient = "";
    this.gradientRequest = 0;
    this.frame = 0;
    this.elapsed = 0;
    this.lastFrameAt = 0;
    this.speed = 1;
    this.speedTarget = 1;
    this.energy = 0;
    this.energyTarget = 0;
    this.isVisible = true;
    this.reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");

    this.render = this.render.bind(this);
    this.resize = this.resize.bind(this);
  }

  connectedCallback() {
    this.syncAttributes();
    this.button.addEventListener("click", this.handleClick);
    this.button.addEventListener("pointerenter", this.handlePointerEnter);
    this.button.addEventListener("pointerleave", this.handlePointerLeave);
    document.addEventListener("visibilitychange", this.handleVisibilityChange);
    this.reducedMotion.addEventListener("change", this.handleMotionPreference);

    this.resizeObserver = new ResizeObserver(this.resize);
    this.resizeObserver.observe(this);

    this.intersectionObserver = new IntersectionObserver(([entry]) => {
      this.isVisible = entry.isIntersecting;
      if (this.isVisible) this.start();
      else this.stop();
    });
    this.intersectionObserver.observe(this);

    try {
      this.setupWebGL();
      this.resize();
      this.start();
    } catch (error) {
      console.warn(error);
      this.button.classList.add("fallback");
      this.canvas.hidden = true;
    }
  }

  disconnectedCallback() {
    this.stop();
    this.button.removeEventListener("click", this.handleClick);
    this.button.removeEventListener("pointerenter", this.handlePointerEnter);
    this.button.removeEventListener("pointerleave", this.handlePointerLeave);
    document.removeEventListener("visibilitychange", this.handleVisibilityChange);
    this.reducedMotion.removeEventListener("change", this.handleMotionPreference);
    this.resizeObserver?.disconnect();
    this.intersectionObserver?.disconnect();
  }

  attributeChangedCallback() {
    this.syncAttributes();
  }

  handleClick = () => {
    this.dispatchEvent(new CustomEvent("play", { bubbles: true, composed: true }));
  };

  handlePointerEnter = () => {
    this.speedTarget = 1;
    this.energyTarget = 0;
  };

  handlePointerLeave = () => {
    this.speedTarget = 1;
    this.energyTarget = 0;
  };

  handleVisibilityChange = () => {
    if (document.hidden) this.stop();
    else this.start();
  };

  handleMotionPreference = () => {
    this.lastFrameAt = 0;
    this.start();
  };

  syncAttributes() {
    if (!this.button) return;
    const gradientId = this.getAttribute("gradient-id");
    const gradientUrl = this.getAttribute("gradient") || "";
    this.button.setAttribute(
      "aria-label",
      this.getAttribute("label") || (gradientId ? `Open ${gradientId} product` : "Open product"),
    );

    if (gradientUrl) {
      this.style.setProperty("--aurora-image", `url(${JSON.stringify(gradientUrl)})`);
    } else {
      this.style.removeProperty("--aurora-image");
    }

    const requestedSize = Number.parseFloat(this.getAttribute("size"));
    if (Number.isFinite(requestedSize) && requestedSize > 0) {
      this.style.setProperty("--aurora-size", `min(${requestedSize}px, calc(100vw - 48px))`);
    }

    if (this.gl && gradientUrl !== this.loadedGradient) {
      this.loadGradient(gradientUrl);
    }
  }

  setupWebGL() {
    const gl = this.canvas.getContext("webgl2", {
      alpha: false,
      antialias: false,
      depth: false,
      powerPreference: "high-performance",
      preserveDrawingBuffer: false,
    });

    if (!gl) throw new Error("WebGL2 is unavailable; using the CSS fallback.");

    const program = createProgram(gl);
    const positions = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positions);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]),
      gl.STATIC_DRAW,
    );

    const positionLocation = gl.getAttribLocation(program, "a_position");
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

    this.gl = gl;
    this.program = program;
    this.uniforms = {
      resolution: gl.getUniformLocation(program, "u_resolution"),
      time: gl.getUniformLocation(program, "u_time"),
      energy: gl.getUniformLocation(program, "u_energy"),
      gradient: gl.getUniformLocation(program, "u_gradient"),
      hasTexture: gl.getUniformLocation(program, "u_has_texture"),
    };
    gl.useProgram(program);
    gl.uniform1i(this.uniforms.gradient, 0);
    gl.uniform1f(this.uniforms.hasTexture, 0);
    this.loadGradient(this.getAttribute("gradient") || "");
  }

  loadGradient(url) {
    if (!this.gl) return;

    const request = ++this.gradientRequest;
    this.loadedGradient = url;
    this.gl.useProgram(this.program);
    this.gl.uniform1f(this.uniforms.hasTexture, 0);

    if (!url) {
      this.start();
      return;
    }

    const image = new Image();
    image.decoding = "async";
    image.crossOrigin = "anonymous";

    image.onload = () => {
      if (request !== this.gradientRequest || !this.gl) return;

      const gl = this.gl;
      this.texture ||= gl.createTexture();
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, this.texture);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.MIRRORED_REPEAT);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.MIRRORED_REPEAT);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
      gl.generateMipmap(gl.TEXTURE_2D);
      gl.useProgram(this.program);
      gl.uniform1f(this.uniforms.hasTexture, 1);
      this.start();
    };

    image.onerror = () => {
      if (request !== this.gradientRequest) return;
      console.warn(`Unable to load gradient texture: ${url}`);
      this.dispatchEvent(
        new CustomEvent("gradient-error", {
          bubbles: true,
          composed: true,
          detail: { url },
        }),
      );
    };

    image.src = url;
  }

  resize() {
    if (!this.gl) return;

    // A 2x DPR ceiling keeps the shader crisp without wasting fill rate on
    // very dense mobile displays.
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const rect = this.getBoundingClientRect();
    const width = Math.max(1, Math.round(rect.width * dpr));
    const height = Math.max(1, Math.round(rect.height * dpr));

    if (this.canvas.width !== width || this.canvas.height !== height) {
      this.canvas.width = width;
      this.canvas.height = height;
      this.gl.viewport(0, 0, width, height);
      this.gl.uniform2f(this.uniforms.resolution, width, height);
    }
  }

  start() {
    if (!this.gl || this.frame || !this.isVisible || document.hidden) return;
    this.lastFrameAt = 0;
    this.frame = requestAnimationFrame(this.render);
  }

  stop() {
    cancelAnimationFrame(this.frame);
    this.frame = 0;
    this.lastFrameAt = 0;
  }

  render(now) {
    if (!this.gl) return;

    const isReduced = this.reducedMotion.matches;
    const delta = this.lastFrameAt ? Math.min((now - this.lastFrameAt) / 1000, 0.05) : 0;
    this.lastFrameAt = now;

    const easing = 1 - Math.exp(-delta * 4.8);
    this.speed += (this.speedTarget - this.speed) * easing;
    this.energy += (this.energyTarget - this.energy) * easing;
    this.elapsed += delta * this.speed;

    this.gl.useProgram(this.program);
    this.gl.uniform1f(this.uniforms.time, this.elapsed);
    this.gl.uniform1f(this.uniforms.energy, this.energy * 0.10);
    this.gl.drawArrays(this.gl.TRIANGLES, 0, 6);

    if (isReduced) {
      this.frame = 0;
      return;
    }

    this.frame = requestAnimationFrame(this.render);
  }
}

const textureTemplate = document.createElement("template");

textureTemplate.innerHTML = `
  <style>
    :host {
      position: absolute;
      inset: 0;
      display: block;
      overflow: hidden;
      background: var(--aurora-image) center / cover no-repeat;
      contain: strict;
      pointer-events: auto;
      transform: translateZ(0);
    }

    canvas {
      display: block;
      width: 100%;
      height: 100%;
    }
  </style>
  <canvas aria-hidden="true"></canvas>
`;

// Every gradient family owns one GPU renderer. All of its visible expressions
// copy from that living source, keeping cards, marks, and small UI crops in
// sync without opening a WebGL context for every component on the page.
class SharedGradientRenderer {
  constructor(url) {
    this.url = url;
    this.canvas = document.createElement("canvas");
    this.canvas.width = 512;
    this.canvas.height = 512;
    this.subscribers = new Set();
    this.energizedBy = new Set();
    this.frame = 0;
    this.elapsed = 0;
    this.lastFrameAt = 0;
    this.speed = 1;
    this.speedTarget = 1;
    this.energy = 0;
    this.energyTarget = 0;
    this.reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    this.render = this.render.bind(this);
    this.handleVisibilityChange = this.handleVisibilityChange.bind(this);
    this.handleMotionPreference = this.handleMotionPreference.bind(this);

    try {
      this.setupWebGL();
      this.loadGradient();
      document.addEventListener("visibilitychange", this.handleVisibilityChange);
      this.reducedMotion.addEventListener("change", this.handleMotionPreference);
    } catch (error) {
      this.failed = true;
      console.warn(error);
    }
  }

  setupWebGL() {
    const gl = this.canvas.getContext("webgl2", {
      alpha: false,
      antialias: false,
      depth: false,
      powerPreference: "high-performance",
      preserveDrawingBuffer: true,
    });

    if (!gl) throw new Error("WebGL2 is unavailable; animated expressions are using image fallbacks.");

    const program = createProgram(gl);
    const positions = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positions);
    gl.bufferData(
      gl.ARRAY_BUFFER,
      new Float32Array([-1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1]),
      gl.STATIC_DRAW,
    );

    const positionLocation = gl.getAttribLocation(program, "a_position");
    gl.enableVertexAttribArray(positionLocation);
    gl.vertexAttribPointer(positionLocation, 2, gl.FLOAT, false, 0, 0);

    this.gl = gl;
    this.program = program;
    this.uniforms = {
      resolution: gl.getUniformLocation(program, "u_resolution"),
      time: gl.getUniformLocation(program, "u_time"),
      energy: gl.getUniformLocation(program, "u_energy"),
      gradient: gl.getUniformLocation(program, "u_gradient"),
      hasTexture: gl.getUniformLocation(program, "u_has_texture"),
    };
    gl.viewport(0, 0, this.canvas.width, this.canvas.height);
    gl.useProgram(program);
    gl.uniform2f(this.uniforms.resolution, this.canvas.width, this.canvas.height);
    gl.uniform1i(this.uniforms.gradient, 0);
    gl.uniform1f(this.uniforms.hasTexture, 0);
  }

  loadGradient() {
    const image = new Image();
    image.decoding = "async";
    image.crossOrigin = "anonymous";
    image.onload = () => {
      if (!this.gl) return;
      const gl = this.gl;
      this.texture = gl.createTexture();
      gl.activeTexture(gl.TEXTURE0);
      gl.bindTexture(gl.TEXTURE_2D, this.texture);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.MIRRORED_REPEAT);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.MIRRORED_REPEAT);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
      gl.generateMipmap(gl.TEXTURE_2D);
      gl.useProgram(this.program);
      gl.uniform1f(this.uniforms.hasTexture, 1);
      this.start();
    };
    image.onerror = () => console.warn(`Unable to load shared gradient texture: ${this.url}`);
    image.src = this.url;
  }

  subscribe(surface) {
    this.subscribers.add(surface);
    this.start();
  }

  unsubscribe(surface) {
    this.subscribers.delete(surface);
    this.energizedBy.delete(surface);
    this.syncEnergy();
    if (!this.subscribers.size) this.stop();
  }

  setEnergized(surface, energized) {
    if (energized) this.energizedBy.add(surface);
    else this.energizedBy.delete(surface);
    this.syncEnergy();
  }

  syncEnergy() {
    this.speedTarget = 1;
    this.energyTarget = 0;
  }

  handleVisibilityChange() {
    if (document.hidden) this.stop();
    else this.start();
  }

  handleMotionPreference() {
    this.lastFrameAt = 0;
    this.start();
  }

  start() {
    if (this.failed || this.frame || !this.subscribers.size || document.hidden) return;
    this.lastFrameAt = 0;
    this.frame = requestAnimationFrame(this.render);
  }

  stop() {
    cancelAnimationFrame(this.frame);
    this.frame = 0;
    this.lastFrameAt = 0;
  }

  render(now) {
    if (!this.gl) return;

    const delta = this.lastFrameAt ? Math.min((now - this.lastFrameAt) / 1000, 0.05) : 0;
    this.lastFrameAt = now;
    const easing = 1 - Math.exp(-delta * 4.8);
    this.speed += (this.speedTarget - this.speed) * easing;
    this.energy += (this.energyTarget - this.energy) * easing;
    this.elapsed += delta * this.speed;

    this.gl.useProgram(this.program);
    this.gl.uniform1f(this.uniforms.time, this.elapsed);
    this.gl.uniform1f(this.uniforms.energy, this.energy * 0.10);
    this.gl.drawArrays(this.gl.TRIANGLES, 0, 6);
    this.subscribers.forEach((surface) => surface.paintFrom(this.canvas));

    if (this.reducedMotion.matches) {
      this.frame = 0;
      return;
    }
    this.frame = requestAnimationFrame(this.render);
  }
}

const sharedGradientRenderers = new Map();

function getSharedGradientRenderer(url) {
  if (!sharedGradientRenderers.has(url)) {
    sharedGradientRenderers.set(url, new SharedGradientRenderer(url));
  }
  return sharedGradientRenderers.get(url);
}

class AuroraTexture extends HTMLElement {
  static observedAttributes = ["gradient"];

  constructor() {
    super();
    this.attachShadow({ mode: "open" }).append(textureTemplate.content.cloneNode(true));
    this.canvas = this.shadowRoot.querySelector("canvas");
    this.context = this.canvas.getContext("2d", { alpha: false });
    this.isVisible = false;
    this.handlePointerEnter = () => this.renderer?.setEnergized(this, true);
    this.handlePointerLeave = () => this.renderer?.setEnergized(this, false);
  }

  connectedCallback() {
    this.syncGradient();
    this.addEventListener("pointerenter", this.handlePointerEnter);
    this.addEventListener("pointerleave", this.handlePointerLeave);
    this.resizeObserver = new ResizeObserver(() => this.renderer?.start());
    this.resizeObserver.observe(this);
    this.intersectionObserver = new IntersectionObserver(([entry]) => {
      this.isVisible = entry.isIntersecting;
      if (this.isVisible) this.renderer?.subscribe(this);
      else this.renderer?.unsubscribe(this);
    }, { rootMargin: "120px" });
    this.intersectionObserver.observe(this);
  }

  disconnectedCallback() {
    this.renderer?.unsubscribe(this);
    this.removeEventListener("pointerenter", this.handlePointerEnter);
    this.removeEventListener("pointerleave", this.handlePointerLeave);
    this.resizeObserver?.disconnect();
    this.intersectionObserver?.disconnect();
  }

  attributeChangedCallback() {
    this.syncGradient();
  }

  syncGradient() {
    const url = this.getAttribute("gradient") || "";
    if (!url || url === this.gradientUrl) return;
    this.renderer?.unsubscribe(this);
    this.gradientUrl = url;
    this.style.setProperty("--aurora-image", `url(${JSON.stringify(url)})`);
    this.renderer = getSharedGradientRenderer(url);
    if (this.renderer.failed) this.canvas.hidden = true;
    if (this.isConnected && this.isVisible) this.renderer.subscribe(this);
  }

  paintFrom(source) {
    if (!this.context || !this.isVisible) return;
    const rect = this.getBoundingClientRect();
    if (!rect.width || !rect.height) return;

    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const width = Math.max(1, Math.round(rect.width * dpr));
    const height = Math.max(1, Math.round(rect.height * dpr));
    if (this.canvas.width !== width || this.canvas.height !== height) {
      this.canvas.width = width;
      this.canvas.height = height;
    }

    const destinationRatio = width / height;
    let sourceWidth = source.width;
    let sourceHeight = source.height;
    let sourceX = 0;
    let sourceY = 0;
    if (destinationRatio > 1) {
      sourceHeight = source.width / destinationRatio;
      sourceY = (source.height - sourceHeight) / 2;
    } else {
      sourceWidth = source.height * destinationRatio;
      sourceX = (source.width - sourceWidth) / 2;
    }
    this.context.drawImage(
      source,
      sourceX,
      sourceY,
      sourceWidth,
      sourceHeight,
      0,
      0,
      width,
      height,
    );
  }
}

if (!customElements.get("aurora-play-button")) {
  customElements.define("aurora-play-button", AuroraPlayButton);
}

if (!customElements.get("aurora-texture")) {
  customElements.define("aurora-texture", AuroraTexture);
}
