"use client";

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { motion, AnimatePresence } from "framer-motion";
import {
  BarChart3,
  ArrowLeft,
  Search,
  CheckCircle2,
  AlertCircle,
  MessageSquare,
  ShieldAlert,
  Calendar,
  Layers,
  ChevronDown,
  ChevronUp,
  ArrowRight,
  ChevronLeft,
  ChevronRight
} from "lucide-react";
import { cn } from "../../lib/utils";

interface EvalLog {
  id: string;
  created_at: string;
  query: string;
  reformulated_query: string;
  context_relevance: number;
  faithfulness: number;
  answer_relevance: number;
  answer: string;
  metadata: any;
}

export default function EvalDashboard() {
  const [logs, setLogs] = useState<EvalLog[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;


  useEffect(() => {
    // Reset to page 1 when filter changes to avoid empty pages
    setCurrentPage(1);
  }, [filter]);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        // Use the server-side proxy route instead of calling backend directly
        // to prevent exposing ADMIN_SECRET_KEY to the browser.
        const response = await fetch("/api/eval-logs");
        if (response.ok) {
          const data = await response.json();
          // The proxy API returns [] on empty or {error: "..."} on fail
          if (Array.isArray(data)) {
             setLogs(data);
          } else {
             console.error("Dashboard page: received non-array response", data);
          }
        } else {
           console.error("Dashboard server-side proxy responded with error status", response.status);
        }
      } catch (error) {
        console.error("Failed to fetch evaluation logs", error);
      } finally {
        setLoading(false);
      }
    };
    fetchLogs();
  }, []);

  const filteredLogs = logs.filter(log =>
    log.query.toLowerCase().includes(filter.toLowerCase()) ||
    log.answer.toLowerCase().includes(filter.toLowerCase())
  );

  // Pagination logic
  const totalPages = Math.ceil(filteredLogs.length / itemsPerPage);
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentLogs = filteredLogs.slice(indexOfFirstItem, indexOfLastItem);

  const averages = {
    faithfulness: logs.length ? logs.reduce((acc, log) => acc + (log.faithfulness || 0), 0) / logs.length : 0,
    relevance: logs.length ? logs.reduce((acc, log) => acc + (log.answer_relevance || 0), 0) / logs.length : 0,
    context: logs.length ? logs.reduce((acc, log) => acc + (log.context_relevance || 0), 0) / logs.length : 0,
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.7) return "text-emerald-400 border-emerald-500/20 bg-emerald-500/5";
    if (score >= 0.4) return "text-amber-400 border-amber-500/20 bg-amber-500/5";
    return "text-rose-400 border-rose-500/20 bg-rose-500/5";
  };

  const stats = [
    { label: "전체 평가 수", value: logs.length, icon: Layers, color: "text-blue-400" },
    { label: "평균 신뢰성 (Faithfulness)", value: `${(averages.faithfulness * 100).toFixed(1)}%`, icon: CheckCircle2, color: "text-emerald-400", score: averages.faithfulness },
    { label: "평균 적합성 (Relevance)", value: `${(averages.relevance * 100).toFixed(1)}%`, icon: BarChart3, color: "text-amber-400", score: averages.relevance },
    { label: "평균 컨텍스트 정확도", value: `${(averages.context * 100).toFixed(1)}%`, icon: Search, color: "text-purple-400", score: averages.context },
  ];

  return (
    <div className="min-h-screen bg-[#0f0f12] text-slate-200 p-8 font-sans">
      <div className="max-w-7xl mx-auto space-y-12">
        {/* Header */}
        <header className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <Link href="/" className="inline-flex items-center text-slate-500 hover:text-slate-300 transition-colors text-sm font-medium gap-2">
              <ArrowLeft className="w-4 h-4" /> 채팅으로 돌아가기
            </Link>
            <h1 className="text-4xl font-bold tracking-tight bg-gradient-to-r from-white to-slate-500 bg-clip-text text-transparent">
              RAG Evaluation Dashboard
            </h1>
            <p className="text-slate-400 max-w-lg">
              LangGraph 워크플로우와 RAGAS 평가지표를 연동한 실시간 시스템 성능 대시보드입니다.
              <br />
              <span className="text-xs text-amber-500/80 font-medium">
                ※ 평가 및 분석이 완료되는 데 약 20초 이상의 시간이 소요될 수 있습니다.
              </span>
            </p>
          </div>
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            <input
              type="text"
              placeholder="질문 검색..."
              className="bg-[#1a1a20] border border-slate-800 rounded-full py-2.5 pl-10 pr-6 w-full md:w-80 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/30 transition-all"
              value={filter}
              onChange={(e) => setFilter(e.target.value)}
            />
          </div>
        </header>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((stat, i) => (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              key={stat.label}
              className="p-6 rounded-3xl bg-[#16161a] border border-slate-800/50 hover:border-slate-700 transition-colors group"
            >
              <div className="flex items-center justify-between mb-4">
                <div className={cn("p-2 rounded-xl bg-slate-800/50 group-hover:scale-110 transition-transform", stat.color)}>
                  <stat.icon className="w-5 h-5" />
                </div>
                {stat.score !== undefined && (
                  <div className={cn("text-[10px] font-bold px-2 py-0.5 rounded-full border uppercase tracking-widest",
                    stat.score >= 0.7 ? "border-emerald-500/30 text-emerald-400 bg-emerald-500/5" : "border-slate-800 text-slate-500"
                  )}>
                    Healthy
                  </div>
                )}
              </div>
              <p className="text-slate-500 text-sm font-medium mb-1">{stat.label}</p>
              <h3 className="text-2xl font-bold tabular-nums text-white tracking-tight">{stat.value}</h3>
            </motion.div>
          ))}
        </div>

        {/* Evaluation Table */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold flex items-center gap-2">
              <Calendar className="w-5 h-5 text-emerald-400" /> 최근 평가 로그
            </h2>
            <div className="text-[12px] text-slate-500 font-mono">
              Total {filteredLogs.length} entries filtered
            </div>
          </div>

          <div className="overflow-hidden rounded-3xl border border-slate-800 bg-[#16161a]">
            {loading ? (
              <div className="py-20 flex flex-col items-center gap-4 text-slate-500 justify-center">
                <div className="w-8 h-8 rounded-full border-2 border-slate-800 border-t-emerald-500 animate-spin" />
                데이터를 불러오고 있습니다...
              </div>
            ) : filteredLogs.length === 0 ? (
              <div className="py-20 text-center text-slate-500">데이터가 없습니다.</div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left text-sm border-collapse">
                  <thead>
                    <tr className="border-b border-slate-800 bg-slate-900/40">
                      <th className="px-6 py-4 font-semibold text-slate-400">질문 (원본/재구성)</th>
                      <th className="px-6 py-4 font-semibold text-slate-400 text-center w-32">Faithfulness</th>
                      <th className="px-6 py-4 font-semibold text-slate-400 text-center w-32">Relevance</th>
                      <th className="px-6 py-4 font-semibold text-slate-400 text-center w-24">Context</th>
                      <th className="px-6 py-4 font-semibold text-slate-400 w-20 text-right">기능</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/50">
                    {currentLogs.map((log) => (
                      <React.Fragment key={log.id}>
                        <tr 
                          className={cn(
                            "hover:bg-slate-800/30 transition-colors group",
                            expandedId === log.id && "bg-slate-800/40"
                          )}
                        >
                          <td className="px-6 py-4">
                            <div className="space-y-1.5 max-w-md">
                              <p className="font-semibold text-slate-200 truncate group-hover:text-white transition-colors">
                                {log.query}
                              </p>
                              <p className="text-[11px] text-slate-500 font-mono">
                                {log.reformulated_query || 'N/A'}
                              </p>
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <div className={cn("px-3 py-1.5 rounded-xl border text-center font-bold text-xs", getScoreColor(log.faithfulness))}>
                              {(log.faithfulness * 100).toFixed(0)}%
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <div className={cn("px-3 py-1.5 rounded-xl border text-center font-bold text-xs", getScoreColor(log.answer_relevance))}>
                              {(log.answer_relevance * 100).toFixed(0)}%
                            </div>
                          </td>
                          <td className="px-6 py-4">
                            <div className={cn("px-2 py-0.5 rounded-full border text-center font-bold text-[10px]",
                              log.context_relevance > 0.5 ? "border-purple-500/20 text-purple-400 bg-purple-500/5" : "border-slate-800 text-slate-500"
                            )}>
                              {log.context_relevance > 0.5 ? 'FOUND' : 'MISSING'}
                            </div>
                          </td>
                          <td className="px-6 py-4 text-right">
                            <button
                              onClick={() => setExpandedId(expandedId === log.id ? null : log.id)}
                              aria-expanded={expandedId === log.id}
                              aria-controls={`details-${log.id}`}
                              className="flex items-center justify-end w-full py-2 hover:opacity-70 transition-all focus:outline-none focus:ring-2 focus:ring-emerald-500/50 rounded-lg"
                              title={expandedId === log.id ? "숨기기" : "자세히 보기"}
                            >
                              {expandedId === log.id ? <ChevronUp className="w-5 h-5 text-emerald-400" /> : <ChevronDown className="w-5 h-5 text-slate-600 group-hover:text-slate-400" />}
                            </button>
                          </td>
                        </tr>
                        <AnimatePresence>
                          {expandedId === log.id && (
                            <tr>
                              <td colSpan={5} className="p-0 border-none bg-slate-900/60">
                                <motion.div
                                  id={`details-${log.id}`}
                                  initial={{ height: 0, opacity: 0 }}
                                  animate={{ height: 'auto', opacity: 1 }}
                                  exit={{ height: 0, opacity: 0 }}
                                  className="overflow-hidden"
                                >
                                  <div className="p-8 space-y-6 border-l-2 border-emerald-500/40 ml-6 mr-6 my-4 bg-black/20 rounded-2xl">
                                    <div className="space-y-2">
                                      <h4 className="text-xs font-bold text-emerald-400 uppercase tracking-widest flex items-center gap-2">
                                        <ArrowRight className="w-3 h-3" /> User Question
                                      </h4>
                                      <p className="text-slate-200 font-medium text-lg leading-relaxed">{log.query}</p>
                                    </div>
                                    <div className="space-y-3">
                                      <h4 className="text-xs font-bold text-blue-400 uppercase tracking-widest flex items-center gap-2">
                                        <ArrowRight className="w-3 h-3" /> PhiloRAG Answer
                                      </h4>
                                      <div className="bg-slate-950/50 p-6 rounded-xl border border-slate-800/50 text-slate-300 leading-relaxed whitespace-pre-wrap shadow-inner">
                                        {log.answer}
                                      </div>
                                    </div>
                                    <div className="flex gap-8 text-[11px] font-mono text-slate-500 pt-4 border-t border-slate-800/50">
                                      <div>ID: <span className="text-slate-400">{log.id}</span></div>
                                      <div>Created: <span className="text-slate-400">{new Date(log.created_at).toLocaleString()}</span></div>
                                    </div>
                                  </div>
                                </motion.div>
                              </td>
                            </tr>
                          )}
                        </AnimatePresence>
                      </React.Fragment>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>

          {/* Pagination Controls */}
          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2 pt-4">
              <button
                onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                disabled={currentPage === 1}
                className="p-2 rounded-lg border border-slate-800 hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                <ChevronLeft className="w-5 h-5" />
              </button>
              <div className="flex gap-1">
                {Array.from({ length: Math.min(5, totalPages) }, (_, i) => {
                  const pageNum = i + 1;
                  return (
                    <button
                      key={pageNum}
                      onClick={() => setCurrentPage(pageNum)}
                      className={cn(
                        "w-10 h-10 rounded-lg border text-sm font-semibold transition-all",
                        currentPage === pageNum 
                          ? "bg-emerald-500/10 border-emerald-500/40 text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]" 
                          : "border-slate-800 text-slate-500 hover:border-slate-600 hover:text-slate-300"
                      )}
                    >
                      {pageNum}
                    </button>
                  );
                })}
                {totalPages > 5 && <span className="w-10 h-10 flex items-center justify-center text-slate-600">...</span>}
              </div>
              <button
                onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                disabled={currentPage === totalPages}
                className="p-2 rounded-lg border border-slate-800 hover:bg-slate-800 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
              >
                <ChevronRight className="w-5 h-5" />
              </button>
            </div>
          )}
        </section>

        {/* Analysis Card */}
        <section className="bg-gradient-to-br from-emerald-500/10 via-transparent to-blue-500/10 rounded-3xl p-8 border border-slate-800 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-8 opacity-10">
            <ShieldAlert className="w-24 h-24" />
          </div>
          <div className="relative z-10 space-y-4 max-w-2xl">
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <MessageSquare className="w-6 h-6 text-blue-400" /> AI 성능 분석 코멘트
            </h2>
            <p className="text-slate-400 leading-relaxed">
              최근 평가 데이터를 기반으로 볼 때, 현재 시스템은 제공된 철학 구절에 대한 충성도(Faithfulness)가 높게 유지되고 있습니다.
              다만, 한국어 질문에 대한 관련성(Relevance) 점수가 평소보다 낮게 측정될 수 있으며, 이는 임베딩 모델의 한계로 인해 TODO 리스트에 다국어 지원 모델 교체가 예정되어 있습니다.
            </p>
            <div className="pt-4 flex items-center gap-4">
              <div className="flex items-center gap-2 text-xs font-semibold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
                <CheckCircle2 className="w-3 h-3" /> 환각 방지 활성화됨
              </div>
              <div className="flex items-center gap-2 text-xs font-semibold text-amber-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20">
                <AlertCircle className="w-3 h-3" /> 평가 모델 개선 필요
              </div>
            </div>
          </div>
        </section>
      </div>

      {/* Footer Nav */}
      <footer className="mt-20 py-10 border-t border-slate-900 text-center">
        <p className="text-slate-600 text-xs font-mono tracking-widest uppercase">
          PhiloRAG Performance Monitor v0.1.0 • Built with NextJS 16
        </p>
      </footer>
    </div>
  );
}
