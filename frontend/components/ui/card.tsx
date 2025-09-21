import { ReactNode } from "react";

export function Card({ className = "", children }: { className?: string; children: ReactNode }) {
	return <div className={`rounded-lg border border-gray-200 bg-white shadow-sm ${className}`}>{children}</div>;
}

export function CardContent({ className = "", children }: { className?: string; children: ReactNode }) {
	return <div className={`p-6 ${className}`}>{children}</div>;
}


