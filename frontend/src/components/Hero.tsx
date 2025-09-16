"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Canvas } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { Suspense } from "react";

export default function Hero() {
  return (
    <section className="min-h-screen bg-gradient-to-br from-[#0f0c29] via-[#302b63] to-[#24243e] text-white flex items-center justify-center relative overflow-hidden">
      {/* Left Side: Text + Buttons */}
      <div className="max-w-2xl px-6 z-10">
        <motion.h1
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="text-5xl font-extrabold leading-tight mb-4"
        >
          AutoBiz.AI
        </motion.h1>
        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 1 }}
          className="text-xl mb-8"
        >
          Automate your business with real AI Agents — Reports, Emails, Dashboards.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 1 }}
          className="flex gap-4"
        >
          <Button className="bg-blue-600 hover:bg-blue-700 text-lg">📤 Upload CSV</Button>
          <Button variant="outline" className="text-white border-white text-lg">
            💬 Talk to Agent
          </Button>
        </motion.div>
      </div>

      {/* Right Side: 3D Box */}
      <div className="absolute right-10 w-[400px] h-[400px] z-0">
        <Canvas camera={{ position: [2, 2, 2] }}>
          <ambientLight intensity={1.5} />
          <pointLight position={[5, 5, 5]} />
          <Suspense fallback={null}>
            <mesh rotation={[0.4, 0.2, 0.1]}>
              <boxGeometry args={[1.5, 1.5, 1.5]} />
              <meshStandardMaterial color={"#00ffff"} wireframe />
            </mesh>
            <OrbitControls enableZoom={false} autoRotate />
          </Suspense>
        </Canvas>
      </div>
    </section>
  );
}
