"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { MatchmakingDashboard } from "@/components/matchmaking-dashboard"
import { VoiceChatOverlay } from "@/components/voice-chat-overlay"
import { AntiCheatPanel } from "@/components/anti-cheat-panel"
import { MatchAnalytics } from "@/components/match-analytics"
import { ShadowSyncBanner } from "@/components/shadow-sync-banner"

export default function Home() {
  const [activeTab, setActiveTab] = useState("matchmaking")

  return (
    <main className="relative min-h-screen bg-background overflow-hidden">
      <div className="fixed inset-0 z-0 opacity-20">
        <div className="absolute inset-0 bg-gradient-to-t from-background to-transparent z-10" />
        <div
          className="w-full h-full bg-cover bg-center"
          style={{ backgroundImage: "url('/images/background.png')" }}
        />
      </div>

      <SidebarProvider>
        <div className="flex h-screen relative z-10">
          <AppSidebar />
          <div className="flex-1 flex flex-col overflow-hidden">
            <header className="border-b border-border/40 bg-background/60 backdrop-blur-xl p-4 md:p-6 flex flex-wrap md:flex-nowrap items-center justify-between gap-4">
              <div className="flex items-center gap-3">
                <img src="/images/logo.png" alt="GhostLAN Logo" className="w-8 h-8" />
                <h1 className="text-xl md:text-2xl font-bold text-primary">GhostLAN</h1>
              </div>
              <ShadowSyncBanner />
              <div className="hidden md:block text-sm">Status: Online</div>
            </header>

            <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
              <TabsList className="bg-background/50 backdrop-blur-sm border-b border-border/40 px-2 md:px-6 h-12 overflow-x-auto">
                <TabsTrigger
                  value="matchmaking"
                  className="data-[state=active]:text-primary data-[state=active]:shadow-[0_0_10px_theme(colors.primary)]"
                >
                  LAN Matchmaking
                </TabsTrigger>
                <TabsTrigger
                  value="analytics"
                  className="data-[state=active]:text-primary data-[state=active]:shadow-[0_0_10px_theme(colors.primary)]"
                >
                  Match Analytics
                </TabsTrigger>
                <TabsTrigger
                  value="anticheat"
                  className="data-[state=active]:text-primary data-[state=active]:shadow-[0_0_10px_theme(colors.primary)]"
                >
                  Anti-Cheat
                </TabsTrigger>
              </TabsList>

              <div className="flex-1 overflow-hidden">
                <TabsContent value="matchmaking" className="h-full">
                  <MatchmakingDashboard />
                </TabsContent>
                <TabsContent value="analytics" className="h-full">
                  <MatchAnalytics />
                </TabsContent>
                <TabsContent value="anticheat" className="h-full">
                  <AntiCheatPanel />
                </TabsContent>
              </div>
            </Tabs>
          </div>

          <VoiceChatOverlay />
        </div>
      </SidebarProvider>
    </main>
  )
}
