import {useEffect, useRef} from "react";
import "../mez-global-navigation.js";
import "../mez-global-navigation.css";

export function MezGlobalNavigation({selected="aios", onProductNavigate}) {
  const ref=useRef(null);
  useEffect(()=>{
    const node=ref.current;
    const handle=event=>onProductNavigate?.(event.detail);
    node?.addEventListener("mez-product-navigate",handle);
    return()=>node?.removeEventListener("mez-product-navigate",handle);
  },[onProductNavigate]);
  return <mez-global-navigation ref={ref} selected={selected} home-href="/" systems-href="/systems/" about-href="/about/" />;
}
