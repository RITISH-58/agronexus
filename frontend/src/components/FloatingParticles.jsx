import React, { useMemo } from 'react';

const FloatingParticles = () => {
    const leaves = useMemo(() => {
        return Array.from({ length: 15 }).map((_, i) => ({
            id: `leaf-${i}`,
            size: Math.random() * 8 + 8, // 8px to 16px
            left: `${Math.random() * 100}%`,
            animationDuration: `${Math.random() * 15 + 15}s`, // 15s to 30s
            animationDelay: `-${Math.random() * 20}s`, // start at various points
            opacity: Math.random() * 0.4 + 0.1, // 0.1 to 0.5
        }));
    }, []);

    const motes = useMemo(() => {
        return Array.from({ length: 30 }).map((_, i) => ({
            id: `mote-${i}`,
            size: Math.random() * 3 + 1, // 1px to 4px
            left: `${Math.random() * 100}%`,
            animationDuration: `${Math.random() * 20 + 20}s`, // 20s to 40s
            animationDelay: `-${Math.random() * 30}s`,
            opacity: Math.random() * 0.3 + 0.1,
        }));
    }, []);

    return (
        <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden bg-gradient-to-br from-[#F1F8E9] to-[#E8F5E9]">
            {/* Subtle green tint overlay */}
            <div className="absolute inset-0 bg-[#C8E6C9] mix-blend-multiply opacity-10"></div>
            
            {/* Leaves */}
            {leaves.map((leaf) => (
                <div
                    key={leaf.id}
                    className="absolute animate-leaf-float opacity-0"
                    style={{
                        left: leaf.left,
                        width: `${leaf.size}px`,
                        height: `${leaf.size}px`,
                        animationDuration: leaf.animationDuration,
                        animationDelay: leaf.animationDelay,
                        filter: `opacity(${leaf.opacity * 100}%) brightness(0.9) sepia(0.5) hue-rotate(60deg)`
                    }}
                >
                    <svg viewBox="0 0 24 24" fill="currentColor" className="text-green-600/30">
                        <path d="M17,8C8,10 5.9,16.17 3.82,21.34L5.71,22L6.66,19.7C7.14,19.87 7.64,20 8,20C19,20 22,3 22,3C21,5 14,5.25 9,6.25C4,7.25 7,11.5 7,11.5C7,11.5 10.5,5.5 17,8Z" />
                    </svg>
                </div>
            ))}

            {/* Light Dust/Pollen */}
            {motes.map((mote) => (
                <div
                    key={mote.id}
                    className="absolute rounded-full bg-white animate-leaf-float opacity-0 shadow-[0_0_4px_rgba(255,255,255,0.8)]"
                    style={{
                        left: mote.left,
                        width: `${mote.size}px`,
                        height: `${mote.size}px`,
                        animationDuration: mote.animationDuration,
                        animationDelay: mote.animationDelay,
                        filter: `opacity(${mote.opacity * 100}%) blur(0.5px)`
                    }}
                ></div>
            ))}

            {/* Soft wave motion at the bottom (implied field) */}
            <div className="absolute bottom-[-10%] left-[-5%] right-[-5%] h-[30%] bg-gradient-to-t from-[#C8E6C9]/20 to-transparent animate-wave rounded-[100%] blur-[20px] mix-blend-multiply"></div>
        </div>
    );
};

export default FloatingParticles;
