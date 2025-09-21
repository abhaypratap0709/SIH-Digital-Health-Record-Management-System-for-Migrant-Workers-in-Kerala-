"use client";

import { useState, useEffect } from "react";
import QRCode from "qrcode.react";
import { Card, CardContent } from "@/components/ui/card";

type Report = {
	date: string;
	file: string;
	medicine?: string;
};

export default function WorkerPage() {
	const [consent, setConsent] = useState(false);
	const [reports, setReports] = useState<Report[]>([]);
	const [loading, setLoading] = useState(true);

	const workerName = "Worker Name";
	const phid = "123456";
	const workerId = 1;

	useEffect(() => {
		let cancelled = false;

		(async () => {
			try {
				const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
				const res = await fetch(`${base}/reports/${workerId}`, { cache: "no-store" });
				if (!res.ok) throw new Error(`HTTP ${res.status}`);
				const data = await res.json();
				if (!cancelled) setReports(data);
			} catch (err) {
				console.error("Error fetching reports:", err);
			} finally {
				if (!cancelled) setLoading(false);
			}
		})();

		return () => {
			cancelled = true;
		};
	}, [workerId]);

	if (loading) {
		return <div className="p-4 animate-pulse">Loading...</div>;
	}

	return (
		<div className="p-4 space-y-4">
			<div>
				<h1 className="text-2xl font-bold">{workerName}</h1>
				<p>PHID: {phid}</p>
			</div>

			<QRCode value={`${workerName} - PHID: ${phid}`} />

			<div className="space-y-2">
				{reports.map((report, idx) => (
					<Card key={idx} className="p-4">
						<CardContent className="p-0 space-y-1">
							<p>Date: {report.date}</p>
							<p>File: {report.file}</p>
							<p>Medicine: {report.medicine ?? "-"}</p>
						</CardContent>
					</Card>
				))}
			</div>

			<label className="flex items-center gap-2">
				<span>Consent: {consent ? "Yes" : "No"}</span>
				<input
					type="checkbox"
					checked={consent}
					onChange={() => setConsent((v) => !v)}
					className="h-4 w-4"
				/>
			</label>
		</div>
	);
}


