export const SHAPES = Object.freeze({ disc: 0, sphere: 1, rect: 2, wings: 3 });

const VERTEX_SHADER = "attribute vec2 aPos; void main(){ gl_Position = vec4(aPos,0.,1.); }";
const FRAGMENT_SHADER = `
precision highp float;

uniform vec2 uRes;
uniform float uTime;
uniform float uDpr;
uniform vec3 uC[4];
uniform vec2 uA[4];
uniform float uW[4];
uniform vec4 uBloomSel;
uniform vec3 uShade;
uniform vec3 uBloom;
uniform int uShape;
uniform float uRadius;
uniform float uOct;
uniform sampler2D uMask;

vec3 mod289(vec3 x){ return x-floor(x*(1.0/289.0))*289.0; }
vec4 mod289(vec4 x){ return x-floor(x*(1.0/289.0))*289.0; }
vec4 permute(vec4 x){ return mod289(((x*34.0)+1.0)*x); }
vec4 taylorInvSqrt(vec4 r){ return 1.79284291400159-0.85373472095314*r; }

float snoise(vec3 v){
  const vec2 C=vec2(1.0/6.0,1.0/3.0);
  const vec4 D=vec4(0.0,0.5,1.0,2.0);
  vec3 i=floor(v+dot(v,C.yyy));
  vec3 x0=v-i+dot(i,C.xxx);
  vec3 g=step(x0.yzx,x0.xyz);
  vec3 l=1.0-g;
  vec3 i1=min(g.xyz,l.zxy);
  vec3 i2=max(g.xyz,l.zxy);
  vec3 x1=x0-i1+C.xxx;
  vec3 x2=x0-i2+C.yyy;
  vec3 x3=x0-D.yyy;
  i=mod289(i);
  vec4 p=permute(permute(permute(
    i.z+vec4(0.0,i1.z,i2.z,1.0))
    +i.y+vec4(0.0,i1.y,i2.y,1.0))
    +i.x+vec4(0.0,i1.x,i2.x,1.0));
  float n_=0.142857142857;
  vec3 ns=n_*D.wyz-D.xzx;
  vec4 j=p-49.0*floor(p*ns.z*ns.z);
  vec4 x_=floor(j*ns.z);
  vec4 y_=floor(j-7.0*x_);
  vec4 x=x_*ns.x+ns.yyyy;
  vec4 y=y_*ns.x+ns.yyyy;
  vec4 h=1.0-abs(x)-abs(y);
  vec4 b0=vec4(x.xy,y.xy);
  vec4 b1=vec4(x.zw,y.zw);
  vec4 s0=floor(b0)*2.0+1.0;
  vec4 s1=floor(b1)*2.0+1.0;
  vec4 sh=-step(h,vec4(0.0));
  vec4 a0=b0.xzyw+s0.xzyw*sh.xxyy;
  vec4 a1=b1.xzyw+s1.xzyw*sh.zzww;
  vec3 p0=vec3(a0.xy,h.x);
  vec3 p1=vec3(a0.zw,h.y);
  vec3 p2=vec3(a1.xy,h.z);
  vec3 p3=vec3(a1.zw,h.w);
  vec4 norm=taylorInvSqrt(vec4(dot(p0,p0),dot(p1,p1),dot(p2,p2),dot(p3,p3)));
  p0*=norm.x; p1*=norm.y; p2*=norm.z; p3*=norm.w;
  vec4 m=max(0.6-vec4(dot(x0,x0),dot(x1,x1),dot(x2,x2),dot(x3,x3)),0.0);
  m=m*m;
  return 42.0*dot(m*m,vec4(dot(p0,x0),dot(p1,x1),dot(p2,x2),dot(p3,x3)));
}

float fbm(vec3 p){
  float v=0.0;
  float a=0.5;
  for(int i=0;i<3;i++){
    if(float(i)>=uOct) break;
    v+=a*snoise(p);
    p=p*2.02+vec3(11.7,5.3,2.9);
    a*=0.5;
  }
  return v;
}

vec3 toLinear(vec3 c){ return pow(c,vec3(2.2)); }
vec3 toSRGB(vec3 c){ return pow(max(c,0.0),vec3(1.0/2.2)); }

float hash21(vec2 p){
  p=fract(p*vec2(123.34,456.21));
  p+=dot(p,p+45.32);
  return fract(p.x*p.y);
}

float sdRoundBox(vec2 p,vec2 b,float r){
  vec2 q=abs(p)-b+r;
  return min(max(q.x,q.y),0.0)+length(max(q,0.0))-r;
}

void main(){
  vec2 frag=gl_FragCoord.xy;
  float mn=min(uRes.x,uRes.y);
  vec2 uv=(frag-0.5*uRes)/mn;
  float rad=length(uv)*2.0;
  float aa=1.5/mn;
  float alpha;

  if(uShape==3){
    vec2 tuv=frag/uRes;
    alpha=texture2D(uMask,vec2(tuv.x,1.0-tuv.y)).a;
  }else if(uShape==2){
    vec2 halfExt=uRes/mn*0.5;
    float d=sdRoundBox(uv,halfExt,uRadius*0.5);
    alpha=1.0-smoothstep(-aa,aa,d);
  }else{
    alpha=1.0-smoothstep(0.5-aa,0.5+aa,length(uv));
  }
  if(alpha<=0.001){ gl_FragColor=vec4(0.0); return; }

  vec3 p=vec3(uv*0.95,uTime*0.075);
  vec2 q=vec2(fbm(p),fbm(p+vec3(3.71,1.33,0.0)));
  vec2 r=vec2(
    fbm(p+1.15*vec3(q,0.0)+vec3(1.7,9.2,uTime*0.055)),
    fbm(p+1.15*vec3(q,0.0)+vec3(8.3,2.8,uTime*0.066))
  );
  vec2 warped=uv+0.42*r+0.16*q;

  float weights[4];
  float weightSum=1e-5;
  for(int i=0;i<4;i++){
    float fi=float(i);
    vec2 moving=uA[i]+vec2(
      cos(uTime*(0.079+fi*0.016)+fi*1.7),
      sin(uTime*(0.083+fi*0.014)+fi*2.9)
    )*0.23;
    float distanceSq=dot(warped-moving,warped-moving);
    weights[i]=pow(exp(-distanceSq*7.5),1.9)*uW[i];
    weightSum+=weights[i];
  }

  vec3 colour=vec3(0.0);
  for(int i=0;i<4;i++) colour+=toLinear(uC[i])*weights[i];
  colour/=weightSum;

  float detail=fbm(vec3(warped*2.6,uTime*0.13));
  colour*=1.0+detail*0.17;
  float bloomWeight=dot(vec4(weights[0],weights[1],weights[2],weights[3]),uBloomSel);
  float hot=smoothstep(0.15,0.85,detail*0.5+0.5)*(bloomWeight/weightSum)*2.6;
  colour+=toLinear(uBloom)*clamp(hot,0.0,1.0)*0.20;

  if(uShape==1){
    float rim=smoothstep(0.50,1.08,rad+detail*0.18);
    colour=mix(colour,toLinear(uShade),rim*0.62);
    colour*=1.0+0.10*smoothstep(1.0,-0.5,uv.x*1.7+uv.y*2.0);
    float sphereLum=dot(colour,vec3(0.2126,0.7152,0.0722));
    colour=mix(vec3(sphereLum),colour,1.16);
  }

  colour=toSRGB(colour);
  vec2 grainPoint=gl_FragCoord.xy/max(uDpr,1.0);
  float fine=hash21(grainPoint)-0.5;
  float mottle=(hash21(floor(grainPoint/2.5))-0.5)*0.75;
  float luminosity=dot(colour,vec3(0.2126,0.7152,0.0722));
  float grainMask=1.0-0.70*smoothstep(0.42,0.98,luminosity);
  colour+=(fine*0.085+mottle*0.036)*grainMask;
  colour=min(colour,vec3(0.97));

  gl_FragColor=vec4(colour*alpha,alpha);
}
`;

const DEFAULT_CATALOGUE = new URL("./gradients.json", import.meta.url);
const DEFAULT_STATIC_BASE = new URL("./assets/gradients/", import.meta.url);
const DEFAULT_WINGS = new URL("./assets/wings.svg", import.meta.url);

function hexToRgb(value) {
  const clean = value.replace("#", "");
  return [
    parseInt(clean.slice(0, 2), 16) / 255,
    parseInt(clean.slice(2, 4), 16) / 255,
    parseInt(clean.slice(4, 6), 16) / 255
  ];
}

function normaliseCore(raw, fallbackId) {
  const anchors = raw.anchors || [];
  if (anchors.length !== 4) {
    throw new Error("Living core " + (raw.id || fallbackId) + " must define exactly four anchors");
  }
  const bloomAnchor = Number.isInteger(raw.bloomAnchor) ? raw.bloomAnchor : 0;
  return {
    id: raw.id || raw.gradient || fallbackId,
    file: raw.staticTwin || raw.file,
    anchors: anchors.map(function (anchor) {
      return {
        colour: anchor.hex ? hexToRgb(anchor.hex) : anchor.rgb,
        pos: anchor.pos,
        weight: anchor.weight == null ? 1 : anchor.weight
      };
    }),
    shade: Array.isArray(raw.shade) ? raw.shade : hexToRgb(raw.shade),
    bloom: Array.isArray(raw.bloom) ? raw.bloom : hexToRgb(raw.bloom),
    bloomSelect: [0, 1, 2, 3].map(function (index) { return index === bloomAnchor ? 1 : 0; })
  };
}

function normaliseCatalogue(source) {
  const values = Array.isArray(source) ? source : Object.entries(source.cores || {}).map(function (entry) {
    return Object.assign({ slug: entry[0] }, entry[1]);
  });
  const result = new Map();
  values.forEach(function (raw) {
    const key = raw.slug || raw.id;
    const core = normaliseCore(raw, key);
    result.set(key, core);
    result.set(core.id, core);
    if (raw.gradient) result.set(raw.gradient, core);
  });
  return result;
}

async function readCatalogue(value) {
  if (value) return value;
  const response = await fetch(DEFAULT_CATALOGUE);
  if (!response.ok) throw new Error("Living-core catalogue failed: " + response.status);
  return response.json();
}

function compile(gl, type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    throw new Error(gl.getShaderInfoLog(shader) || "Unknown shader compile error");
  }
  return shader;
}

function setStaticSurface(element, core, shape, radius, staticBase, wingsUrl) {
  const canvas = element.querySelector("canvas[data-mz-core-canvas]");
  if (canvas) canvas.hidden = true;
  const source = new URL(core.file, staticBase).href;
  element.style.backgroundImage = "url('" + source + "')";
  element.style.backgroundSize = "cover";
  element.style.backgroundPosition = "center";
  element.dataset.mzCoreMode = "static";

  element.style.mask = "";
  element.style.webkitMask = "";
  if (shape === SHAPES.disc || shape === SHAPES.sphere) {
    element.style.borderRadius = "50%";
  } else if (shape === SHAPES.rect) {
    const size = Math.min(element.offsetWidth, element.offsetHeight);
    element.style.borderRadius = String(radius * size * 0.5) + "px";
  } else if (shape === SHAPES.wings) {
    const mask = "url('" + wingsUrl.href + "') center / contain no-repeat";
    element.style.mask = mask;
    element.style.webkitMask = mask;
  }
}

class LivingCoreRenderer {
  constructor(cores, options) {
    this.cores = cores;
    this.staticBase = new URL(String(options.staticBaseUrl || DEFAULT_STATIC_BASE), import.meta.url);
    this.wingsUrl = new URL(String(options.wingsUrl || DEFAULT_WINGS), import.meta.url);
    this.canvas = document.createElement("canvas");
    this.disableWebGL = Boolean(options.disableWebGL);
    this.forceShaderFailure = Boolean(options.forceShaderFailure);
    this.gl = this.disableWebGL ? null : this.canvas.getContext("webgl", {
      alpha: true,
      antialias: false,
      depth: false,
      stencil: false,
      premultipliedAlpha: true,
      powerPreference: "high-performance"
    });
    this.surfaces = new Map();
    this.reduced = matchMedia("(prefers-reduced-motion: reduce)");
    this.forceStatic = Boolean(options.forceStatic);
    this.last = 0;
    this.dpr = 1;
    this.ready = false;
    this.failed = false;
    this.frame = this.frame.bind(this);
    this.resize = this.resize.bind(this);
  }

  async initialise() {
    if (!this.gl) {
      console.warn("[mz-core] WebGL unavailable. Static twins active.");
      this.failed = true;
      return;
    }
    try {
      const gl = this.gl;
      this.program = gl.createProgram();
      gl.attachShader(this.program, compile(gl, gl.VERTEX_SHADER, VERTEX_SHADER));
      const fragmentSource = this.forceShaderFailure
        ? FRAGMENT_SHADER + "\nINVALID_SHADER_TOKEN"
        : FRAGMENT_SHADER;
      gl.attachShader(this.program, compile(gl, gl.FRAGMENT_SHADER, fragmentSource));
      gl.linkProgram(this.program);
      if (!gl.getProgramParameter(this.program, gl.LINK_STATUS)) {
        throw new Error(gl.getProgramInfoLog(this.program) || "Unknown shader link error");
      }
      gl.useProgram(this.program);

      const buffer = gl.createBuffer();
      gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
      const position = gl.getAttribLocation(this.program, "aPos");
      gl.enableVertexAttribArray(position);
      gl.vertexAttribPointer(position, 2, gl.FLOAT, false, 0, 0);

      const uniform = function (name) { return gl.getUniformLocation(this.program, name); }.bind(this);
      this.uniforms = {
        resolution: uniform("uRes"),
        time: uniform("uTime"),
        dpr: uniform("uDpr"),
        shade: uniform("uShade"),
        bloom: uniform("uBloom"),
        bloomSelect: uniform("uBloomSel"),
        shape: uniform("uShape"),
        radius: uniform("uRadius"),
        octaves: uniform("uOct"),
        mask: uniform("uMask"),
        colours: [0, 1, 2, 3].map(function (index) { return uniform("uC[" + index + "]"); }),
        anchors: [0, 1, 2, 3].map(function (index) { return uniform("uA[" + index + "]"); }),
        weights: [0, 1, 2, 3].map(function (index) { return uniform("uW[" + index + "]"); })
      };

      await this.createWingsMask();
      gl.clearColor(0, 0, 0, 0);
      this.canvas.addEventListener("webglcontextlost", function (event) {
        event.preventDefault();
        this.failed = true;
        console.error("[mz-core] WebGL context lost. Static twins active.");
        this.applyMode();
      }.bind(this));
      this.reduced.addEventListener("change", this.applyMode.bind(this));
      addEventListener("resize", this.resize);
      document.addEventListener("visibilitychange", function () {
        this.last = 0;
      }.bind(this));
      this.ready = true;
      this.resize();
      this.applyMode();
      requestAnimationFrame(this.frame);
    } catch (error) {
      this.failed = true;
      console.error("[mz-core] Renderer failed. Static twins active.", error);
      this.applyMode();
    }
  }

  async createWingsMask() {
    const image = new Image();
    image.src = this.wingsUrl.href;
    await image.decode();
    const width = 680;
    const height = 482;
    const maskCanvas = document.createElement("canvas");
    maskCanvas.width = width;
    maskCanvas.height = height;
    const context = maskCanvas.getContext("2d");
    context.drawImage(image, 0, 0, width, height);

    const gl = this.gl;
    this.maskTexture = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, this.maskTexture);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, maskCanvas);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, this.maskTexture);
    gl.uniform1i(this.uniforms.mask, 0);
  }

  mount(element, reference, options) {
    const core = this.cores.get(reference);
    if (!core) throw new Error("Unknown living core: " + reference);
    const shape = typeof options.shape === "string" && options.shape in SHAPES
      ? SHAPES[options.shape]
      : Number(options.shape);
    if (!Number.isInteger(shape) || shape < SHAPES.disc || shape > SHAPES.wings) {
      throw new Error("Unknown living-core shape: " + options.shape);
    }
    const radius = Number(options.radius || 0);

    let canvas = element.querySelector("canvas[data-mz-core-canvas]");
    if (!canvas) {
      canvas = document.createElement("canvas");
      canvas.dataset.mzCoreCanvas = "";
      canvas.setAttribute("aria-hidden", "true");
      canvas.style.position = "absolute";
      canvas.style.inset = "0";
      canvas.style.width = "100%";
      canvas.style.height = "100%";
      canvas.style.display = "block";
      element.prepend(canvas);
    }
    element.style.position = element.style.position || "relative";
    element.style.isolation = "isolate";

    const state = {
      element: element,
      canvas: canvas,
      context: canvas.getContext("2d"),
      core: core,
      shape: shape,
      radius: radius,
      speed: 1,
      speedTarget: 1,
      time: 3.2 + Math.random() * 40,
      width: 0,
      height: 0
    };
    element.dataset.mzCoreSpeed = "1";
    element.addEventListener("pointerenter", function () {
      state.speedTarget = 1.85;
      element.dataset.mzCoreSpeed = "1.85";
    });
    element.addEventListener("pointerleave", function () {
      state.speedTarget = 1;
      element.dataset.mzCoreSpeed = "1";
    });
    this.surfaces.set(element, state);
    this.applySurfaceMode(state);
    this.resize();
    return state;
  }

  applySurfaceMode(state) {
    if (this.isStaticMode() || !this.ready) {
      setStaticSurface(state.element, state.core, state.shape, state.radius, this.staticBase, this.wingsUrl);
      return;
    }
    state.canvas.hidden = false;
    state.element.style.backgroundImage = "";
    state.element.style.mask = "";
    state.element.style.webkitMask = "";
    state.element.dataset.mzCoreMode = "live";
  }

  applyMode() {
    this.surfaces.forEach(this.applySurfaceMode.bind(this));
  }

  isStaticMode() {
    return this.forceStatic || this.reduced.matches || this.failed;
  }

  resize() {
    if (!this.gl || this.failed) return;
    this.dpr = Math.min(devicePixelRatio || 1, 2);
    let maxWidth = 1;
    let maxHeight = 1;
    this.surfaces.forEach(function (state) {
      const rect = state.element.getBoundingClientRect();
      maxWidth = Math.max(maxWidth, rect.width);
      maxHeight = Math.max(maxHeight, rect.height);
    });
    const width = Math.min(Math.ceil(maxWidth * this.dpr), 2048);
    const height = Math.min(Math.ceil(maxHeight * this.dpr), 2048);
    if (this.canvas.width !== width || this.canvas.height !== height) {
      this.canvas.width = width;
      this.canvas.height = height;
    }
  }

  frame(milliseconds) {
    requestAnimationFrame(this.frame);
    if (!this.ready || this.isStaticMode() || document.hidden) return;

    const delta = this.last ? Math.min((milliseconds - this.last) / 1000, 1 / 20) : 1 / 60;
    this.last = milliseconds;
    const viewportHeight = innerHeight;
    const viewportWidth = innerWidth;
    const gl = this.gl;
    const uniforms = this.uniforms;
    const framebufferHeight = this.canvas.height;

    this.surfaces.forEach(function (state) {
      const rect = state.element.getBoundingClientRect();
      if (rect.bottom < -40 || rect.top > viewportHeight + 40 || rect.right < 0 || rect.left > viewportWidth) return;
      if (rect.width < 1 || rect.height < 1) return;

      state.speed += (state.speedTarget - state.speed) * (1 - Math.exp(-7 * delta));
      state.time += delta * state.speed;
      const pixelWidth = Math.max(1, Math.round(rect.width * this.dpr));
      const pixelHeight = Math.max(1, Math.round(rect.height * this.dpr));
      if (state.width !== pixelWidth || state.height !== pixelHeight) {
        state.canvas.width = pixelWidth;
        state.canvas.height = pixelHeight;
        state.width = pixelWidth;
        state.height = pixelHeight;
      }

      gl.viewport(0, 0, pixelWidth, pixelHeight);
      gl.uniform2f(uniforms.resolution, pixelWidth, pixelHeight);
      gl.uniform1f(uniforms.time, state.time);
      gl.uniform1f(uniforms.dpr, this.dpr);
      gl.uniform1i(uniforms.shape, state.shape);
      gl.uniform1f(uniforms.radius, state.radius);
      gl.uniform1f(uniforms.octaves, Math.min(rect.width, rect.height) < 90 ? 2 : 3);
      state.core.anchors.forEach(function (anchor, index) {
        gl.uniform3fv(uniforms.colours[index], anchor.colour);
        gl.uniform2fv(uniforms.anchors[index], anchor.pos);
        gl.uniform1f(uniforms.weights[index], anchor.weight);
      });
      gl.uniform3fv(uniforms.shade, state.core.shade);
      gl.uniform3fv(uniforms.bloom, state.core.bloom);
      gl.uniform4fv(uniforms.bloomSelect, state.core.bloomSelect);
      gl.drawArrays(gl.TRIANGLES, 0, 3);

      state.context.clearRect(0, 0, pixelWidth, pixelHeight);
      state.context.drawImage(
        this.canvas,
        0,
        framebufferHeight - pixelHeight,
        pixelWidth,
        pixelHeight,
        0,
        0,
        pixelWidth,
        pixelHeight
      );
    }.bind(this));
  }
}

export async function mountLivingCores(root, options) {
  const settings = options || {};
  const source = await readCatalogue(settings.catalogue);
  const cores = normaliseCatalogue(source);
  const renderer = new LivingCoreRenderer(cores, settings);
  await renderer.initialise();

  const selector = settings.selector || "[data-mz-core], .gx[data-p]";
  const elements = Array.from((root || document).querySelectorAll(selector));
  elements.forEach(function (element) {
    const reference = element.dataset.mzCore || element.dataset.p;
    renderer.mount(element, reference, {
      shape: element.dataset.shape == null ? "disc" : element.dataset.shape,
      radius: element.dataset.radius || 0
    });
  });
  return {
    renderer: renderer,
    count: elements.length,
    mode: renderer.isStaticMode() ? "static" : "live"
  };
}

export async function mountLivingCore(element, coreId, options) {
  const settings = Object.assign({}, options || {});
  const source = await readCatalogue(settings.catalogue);
  const cores = normaliseCatalogue(source);
  const renderer = new LivingCoreRenderer(cores, settings);
  await renderer.initialise();
  renderer.mount(element, coreId, {
    shape: settings.shape || "disc",
    radius: settings.radius || 0
  });
  return renderer;
}
