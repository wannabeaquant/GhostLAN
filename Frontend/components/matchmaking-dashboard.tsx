"use client"

import { useState, useEffect } from "react"
import { Wifi, Users, Clock, Gamepad2, Zap } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Progress } from "@/components/ui/progress"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

// Mock data for nearby players
const MOCK_PLAYERS = [
  { id: 1, name: "CyberNinja", ping: 12, status: "ready", avatar: "/placeholder.svg?height=40&width=40" },
  { id: 2, name: "QuantumFrag", ping: 18, status: "ready", avatar: "/placeholder.svg?height=40&width=40" },
  { id: 3, name: "NeonSniper", ping: 24, status: "waiting", avatar: "/placeholder.svg?height=40&width=40" },
  { id: 4, name: "ShadowByte", ping: 32, status: "waiting", avatar: "/placeholder.svg?height=40&width=40" },
  { id: 5, name: "VirtualPhantom", ping: 8, status: "ready", avatar: "/placeholder.svg?height=40&width=40" },
]

export function MatchmakingDashboard() {
  const [matchStatus, setMatchStatus] = useState<"idle" | "searching" | "connecting" | "ready">("idle")
  const [progress, setProgress] = useState(0)
  const [players, setPlayers] = useState(MOCK_PLAYERS)
  const [scanningLAN, setScanningLAN] = useState(false)

  // Simulate scanning for players
  useEffect(() => {
    if (scanningLAN) {
      const timer = setTimeout(() => {
        setScanningLAN(false)
      }, 3000)
      return () => clearTimeout(timer)
    }
  }, [scanningLAN])

  // Simulate match progress
  useEffect(() => {
    if (matchStatus === "searching") {
      const timer = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            setMatchStatus("connecting")
            clearInterval(timer)
            return 0
          }
          return prev + 5
        })
      }, 200)
      return () => clearInterval(timer)
    }

    if (matchStatus === "connecting") {
      const timer = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            setMatchStatus("ready")
            clearInterval(timer)
            return 100
          }
          return prev + 10
        })
      }, 150)
      return () => clearInterval(timer)
    }
  }, [matchStatus])

  const handleStartMatch = () => {
    if (matchStatus === "idle") {
      setMatchStatus("searching")
    } else if (matchStatus === "ready") {
      // Reset for demo purposes
      setMatchStatus("idle")
      setProgress(0)
    }
  }

  const handleScanLAN = () => {
    setScanningLAN(true)
  }

  return (
    <div className="h-full p-8 overflow-auto grid-bg">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex flex-col md:flex-row gap-6">
          {/* Match Control Panel */}
          <Card className="cyberpunk-card flex-1">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-xl text-primary glow-text">Match Control</CardTitle>
                <Badge
                  variant="outline"
                  className={`
                    ${matchStatus === "idle" ? "border-muted-foreground" : "border-primary animate-pulse-glow"} 
                    px-3 py-1
                  `}
                >
                  {matchStatus === "idle"
                    ? "IDLE"
                    : matchStatus === "searching"
                      ? "SEARCHING"
                      : matchStatus === "connecting"
                        ? "CONNECTING"
                        : "READY"}
                </Badge>
              </div>
              <CardDescription>Configure and launch your LAN match</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-muted/50 p-3 rounded-md flex items-center gap-3">
                  <Users className="text-primary h-5 w-5" />
                  <div>
                    <p className="text-xs text-muted-foreground">Players</p>
                    <p className="font-medium">
                      {players.filter((p) => p.status === "ready").length}/{players.length}
                    </p>
                  </div>
                </div>
                <div className="bg-muted/50 p-3 rounded-md flex items-center gap-3">
                  <Clock className="text-primary h-5 w-5" />
                  <div>
                    <p className="text-xs text-muted-foreground">Est. Wait</p>
                    <p className="font-medium">00:42</p>
                  </div>
                </div>
                <div className="bg-muted/50 p-3 rounded-md flex items-center gap-3">
                  <Gamepad2 className="text-primary h-5 w-5" />
                  <div>
                    <p className="text-xs text-muted-foreground">Game Mode</p>
                    <p className="font-medium">Team Deathmatch</p>
                  </div>
                </div>
                <div className="bg-muted/50 p-3 rounded-md flex items-center gap-3">
                  <Zap className="text-primary h-5 w-5" />
                  <div>
                    <p className="text-xs text-muted-foreground">Network</p>
                    <p className="font-medium">LAN (Local)</p>
                  </div>
                </div>
              </div>

              {(matchStatus === "searching" || matchStatus === "connecting") && (
                <div className="space-y-2">
                  <div className="flex justify-between text-xs">
                    <span>{matchStatus === "searching" ? "Finding players" : "Establishing connection"}</span>
                    <span>{progress}%</span>
                  </div>
                  <Progress value={progress} className="h-2" />
                </div>
              )}
            </CardContent>
            <CardFooter className="flex flex-col sm:flex-row gap-3">
              <Button
                onClick={handleStartMatch}
                className={`w-full sm:w-auto ${matchStatus === "ready" ? "bg-secondary hover:bg-secondary/80" : ""}`}
              >
                {matchStatus === "idle"
                  ? "Start Match"
                  : matchStatus === "searching" || matchStatus === "connecting"
                    ? "Searching..."
                    : "Launch Game"}
              </Button>
              <Button variant="outline" className="w-full sm:w-auto" onClick={handleScanLAN} disabled={scanningLAN}>
                {scanningLAN ? (
                  <>
                    <span className="animate-spin mr-2">◌</span>
                    Scanning...
                  </>
                ) : (
                  <>
                    <Wifi className="mr-2 h-4 w-4" />
                    Scan LAN
                  </>
                )}
              </Button>
            </CardFooter>
          </Card>

          {/* Network Status */}
          <Card className="cyberpunk-card w-full md:w-80">
            <CardHeader>
              <CardTitle className="text-xl">Network Status</CardTitle>
              <CardDescription>LAN connection metrics</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-center py-6">
                <div className="relative flex items-center justify-center">
                  <div className="absolute animate-ping opacity-20 rounded-full h-24 w-24 bg-primary/20"></div>
                  <div className="absolute rounded-full h-20 w-20 bg-primary/10 animate-pulse"></div>
                  <Wifi className="h-10 w-10 text-primary animate-pulse-glow" />
                </div>
              </div>

              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Status</span>
                  <span className="flex items-center gap-1.5">
                    <span className="h-2 w-2 rounded-full bg-green-500"></span>
                    Connected
                  </span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Avg. Ping</span>
                  <span className="text-primary">18ms</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Packet Loss</span>
                  <span>0.2%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-muted-foreground">Bandwidth</span>
                  <span>12.4 MB/s</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Player Cards */}
        <Card className="cyberpunk-card">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl">Nearby Players</CardTitle>
              <Badge variant="outline" className="px-3 py-1">
                {players.length} Found
              </Badge>
            </div>
            <CardDescription>Players discovered on your local network</CardDescription>
          </CardHeader>
          <CardContent className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {players.map((player) => (
                <TooltipProvider key={player.id}>
                  <Tooltip>
                    <TooltipTrigger asChild>
                      <div
                        className={`
                        cyberpunk-card p-6 flex items-center gap-4 transition-all hover-lift cursor-pointer
                        ${player.status === "ready" ? "border-green-500/30 hover:border-green-500/50" : "border-yellow-500/30 hover:border-yellow-500/50"}
                        ${player.status === "ready" ? "hover:bg-green-500/5" : "hover:bg-yellow-500/5"}
                      `}
                      >
                        <Avatar
                          className={`
                          border-2 
                          ${player.status === "ready" ? "border-green-500" : "border-yellow-500"}
                          ${player.status === "ready" ? "animate-pulse-glow" : ""}
                        `}
                        >
                          <AvatarImage src={player.avatar || "/placeholder.svg"} />
                          <AvatarFallback className="bg-muted">{player.name.substring(0, 2)}</AvatarFallback>
                        </Avatar>
                        <div className="flex-1 min-w-0">
                          <p className="font-medium truncate">{player.name}</p>
                          <div className="flex items-center gap-2">
                            <span
                              className={`
                              text-xs px-1.5 py-0.5 rounded-sm
                              ${player.status === "ready" ? "bg-green-500/20 text-green-400" : "bg-yellow-500/20 text-yellow-400"}
                            `}
                            >
                              {player.status.toUpperCase()}
                            </span>
                            <span className="text-xs text-muted-foreground">{player.ping}ms</span>
                          </div>
                        </div>
                      </div>
                    </TooltipTrigger>
                    <TooltipContent side="top">
                      <div className="text-xs space-y-1">
                        <p>
                          <span className="text-muted-foreground">Player:</span> {player.name}
                        </p>
                        <p>
                          <span className="text-muted-foreground">Status:</span> {player.status}
                        </p>
                        <p>
                          <span className="text-muted-foreground">Ping:</span> {player.ping}ms
                        </p>
                        <p>
                          <span className="text-muted-foreground">IP:</span> 192.168.1.{100 + player.id}
                        </p>
                      </div>
                    </TooltipContent>
                  </Tooltip>
                </TooltipProvider>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
