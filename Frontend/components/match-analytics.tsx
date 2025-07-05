"use client"

import { useState } from "react"
import { Trophy, Target, Zap, TrendingUp, Users, Clock } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Progress } from "@/components/ui/progress"

// Mock data for player stats
const PLAYER_STATS = [
  {
    id: 1,
    name: "CyberNinja",
    avatar: "/placeholder.svg?height=40&width=40",
    kills: 24,
    deaths: 8,
    assists: 12,
    accuracy: 68,
    headshots: 9,
    damage: 4850,
    team: "alpha",
  },
  {
    id: 2,
    name: "QuantumFrag",
    avatar: "/placeholder.svg?height=40&width=40",
    kills: 18,
    deaths: 10,
    assists: 15,
    accuracy: 72,
    headshots: 7,
    damage: 3920,
    team: "alpha",
  },
  {
    id: 3,
    name: "NeonSniper",
    avatar: "/placeholder.svg?height=40&width=40",
    kills: 15,
    deaths: 12,
    assists: 8,
    accuracy: 65,
    headshots: 6,
    damage: 3250,
    team: "beta",
  },
  {
    id: 4,
    name: "ShadowByte",
    avatar: "/placeholder.svg?height=40&width=40",
    kills: 21,
    deaths: 9,
    assists: 11,
    accuracy: 70,
    headshots: 8,
    damage: 4120,
    team: "beta",
  },
  {
    id: 5,
    name: "VirtualPhantom",
    avatar: "/placeholder.svg?height=40&width=40",
    kills: 16,
    deaths: 14,
    assists: 9,
    accuracy: 62,
    headshots: 5,
    damage: 3480,
    team: "alpha",
  },
]

export function MatchAnalytics() {
  const [activeTab, setActiveTab] = useState("overview")

  // Calculate team stats
  const alphaTeam = PLAYER_STATS.filter((p) => p.team === "alpha")
  const betaTeam = PLAYER_STATS.filter((p) => p.team === "beta")

  const alphaKills = alphaTeam.reduce((sum, p) => sum + p.kills, 0)
  const betaKills = betaTeam.reduce((sum, p) => sum + p.kills, 0)

  const topPlayer = PLAYER_STATS.reduce((top, player) =>
    player.kills / Math.max(player.deaths, 1) > top.kills / Math.max(top.deaths, 1) ? player : top,
  )

  return (
    <div className="h-full p-8 overflow-auto grid-bg">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Match Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="cyberpunk-card">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Trophy className="h-8 w-8 text-primary" />
                <div>
                  <p className="text-xs text-muted-foreground">Match Winner</p>
                  <p className="font-bold text-primary">Team Alpha</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="cyberpunk-card">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Clock className="h-8 w-8 text-primary" />
                <div>
                  <p className="text-xs text-muted-foreground">Match Duration</p>
                  <p className="font-bold">12:34</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="cyberpunk-card">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <Target className="h-8 w-8 text-primary" />
                <div>
                  <p className="text-xs text-muted-foreground">Total Kills</p>
                  <p className="font-bold">{alphaKills + betaKills}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="cyberpunk-card">
            <CardContent className="p-4">
              <div className="flex items-center gap-3">
                <TrendingUp className="h-8 w-8 text-primary" />
                <div>
                  <p className="text-xs text-muted-foreground">MVP</p>
                  <p className="font-bold">{topPlayer.name}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Analytics Tabs */}
        <Card className="cyberpunk-card">
          <CardHeader>
            <CardTitle className="text-xl">Match Analytics</CardTitle>
            <CardDescription>Detailed performance metrics and insights</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
              <TabsList className="grid w-full grid-cols-3">
                <TabsTrigger value="overview" className="data-[state=active]:text-primary">
                  Overview
                </TabsTrigger>
                <TabsTrigger value="insights" className="data-[state=active]:text-primary">
                  Player Insights
                </TabsTrigger>
                <TabsTrigger value="heatmap" className="data-[state=active]:text-primary">
                  Heatmap
                </TabsTrigger>
              </TabsList>

              <TabsContent value="overview" className="space-y-6">
                {/* Team Comparison */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card className="cyberpunk-card">
                    <CardHeader>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <Users className="h-5 w-5 text-primary" />
                        Team Alpha
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="flex justify-between text-sm">
                        <span>Total Kills</span>
                        <span className="font-bold text-primary">{alphaKills}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Total Deaths</span>
                        <span>{alphaTeam.reduce((sum, p) => sum + p.deaths, 0)}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Avg. Accuracy</span>
                        <span>{Math.round(alphaTeam.reduce((sum, p) => sum + p.accuracy, 0) / alphaTeam.length)}%</span>
                      </div>
                      <Progress value={(alphaKills / (alphaKills + betaKills)) * 100} className="h-2" />
                    </CardContent>
                  </Card>

                  <Card className="cyberpunk-card">
                    <CardHeader>
                      <CardTitle className="text-lg flex items-center gap-2">
                        <Users className="h-5 w-5 text-secondary" />
                        Team Beta
                      </CardTitle>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="flex justify-between text-sm">
                        <span>Total Kills</span>
                        <span className="font-bold text-secondary">{betaKills}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Total Deaths</span>
                        <span>{betaTeam.reduce((sum, p) => sum + p.deaths, 0)}</span>
                      </div>
                      <div className="flex justify-between text-sm">
                        <span>Avg. Accuracy</span>
                        <span>{Math.round(betaTeam.reduce((sum, p) => sum + p.accuracy, 0) / betaTeam.length)}%</span>
                      </div>
                      <Progress value={(betaKills / (alphaKills + betaKills)) * 100} className="h-2" />
                    </CardContent>
                  </Card>
                </div>

                {/* Player Leaderboard */}
                <Card className="cyberpunk-card">
                  <CardHeader>
                    <CardTitle className="text-lg">Player Leaderboard</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {PLAYER_STATS.sort(
                        (a, b) => b.kills / Math.max(b.deaths, 1) - a.kills / Math.max(a.deaths, 1),
                      ).map((player, index) => (
                        <div
                          key={player.id}
                          className={`
  flex items-center gap-6 p-4 rounded-lg border transition-all hover-lift cursor-pointer
  ${player.team === "alpha" ? "border-primary/30 bg-primary/5 hover:bg-primary/10 hover:border-primary/50" : "border-secondary/30 bg-secondary/5 hover:bg-secondary/10 hover:border-secondary/50"}
`}
                        >
                          <div className="flex items-center gap-3">
                            <Badge variant="outline" className="w-8 h-8 rounded-full flex items-center justify-center">
                              {index + 1}
                            </Badge>
                            <Avatar className="h-10 w-10">
                              <AvatarImage src={player.avatar || "/placeholder.svg"} />
                              <AvatarFallback>{player.name.substring(0, 2)}</AvatarFallback>
                            </Avatar>
                            <div>
                              <p className="font-medium">{player.name}</p>
                              <p className="text-xs text-muted-foreground">Team {player.team}</p>
                            </div>
                          </div>

                          <div className="flex-1 grid grid-cols-2 md:grid-cols-6 gap-4 text-sm">
                            <div>
                              <p className="text-xs text-muted-foreground">K/D</p>
                              <p className="font-bold">{(player.kills / Math.max(player.deaths, 1)).toFixed(2)}</p>
                            </div>
                            <div>
                              <p className="text-xs text-muted-foreground">Kills</p>
                              <p className="font-bold text-green-500">{player.kills}</p>
                            </div>
                            <div>
                              <p className="text-xs text-muted-foreground">Deaths</p>
                              <p className="font-bold text-red-500">{player.deaths}</p>
                            </div>
                            <div>
                              <p className="text-xs text-muted-foreground">Assists</p>
                              <p className="font-bold text-blue-500">{player.assists}</p>
                            </div>
                            <div>
                              <p className="text-xs text-muted-foreground">Accuracy</p>
                              <p className="font-bold">{player.accuracy}%</p>
                            </div>
                            <div>
                              <p className="text-xs text-muted-foreground">Damage</p>
                              <p className="font-bold">{player.damage.toLocaleString()}</p>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="insights" className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {PLAYER_STATS.map((player) => (
                    <Card key={player.id} className="cyberpunk-card hover-glow cursor-pointer">
                      <CardHeader className="pb-3">
                        <div className="flex items-center gap-3">
                          <Avatar className="h-10 w-10">
                            <AvatarImage src={player.avatar || "/placeholder.svg"} />
                            <AvatarFallback>{player.name.substring(0, 2)}</AvatarFallback>
                          </Avatar>
                          <div>
                            <CardTitle className="text-base">{player.name}</CardTitle>
                            <CardDescription>Team {player.team}</CardDescription>
                          </div>
                        </div>
                      </CardHeader>
                      <CardContent className="space-y-3">
                        <div className="grid grid-cols-2 gap-3 text-sm">
                          <div className="bg-muted/50 p-2 rounded">
                            <p className="text-xs text-muted-foreground">K/D Ratio</p>
                            <p className="font-bold">{(player.kills / Math.max(player.deaths, 1)).toFixed(2)}</p>
                          </div>
                          <div className="bg-muted/50 p-2 rounded">
                            <p className="text-xs text-muted-foreground">Headshots</p>
                            <p className="font-bold">{player.headshots}</p>
                          </div>
                          <div className="bg-muted/50 p-2 rounded">
                            <p className="text-xs text-muted-foreground">Accuracy</p>
                            <p className="font-bold">{player.accuracy}%</p>
                          </div>
                          <div className="bg-muted/50 p-2 rounded">
                            <p className="text-xs text-muted-foreground">Damage</p>
                            <p className="font-bold">{(player.damage / 1000).toFixed(1)}k</p>
                          </div>
                        </div>

                        <div className="space-y-2">
                          <div className="flex justify-between text-xs">
                            <span>Performance Score</span>
                            <span>
                              {Math.round((player.kills * 2 + player.assists - player.deaths + player.accuracy) / 2)}
                            </span>
                          </div>
                          <Progress
                            value={Math.min(
                              100,
                              (player.kills * 2 + player.assists - player.deaths + player.accuracy) / 2,
                            )}
                            className="h-2"
                          />
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </TabsContent>

              <TabsContent value="heatmap" className="space-y-6">
                <Card className="cyberpunk-card">
                  <CardHeader>
                    <CardTitle className="text-lg">Combat Heatmap</CardTitle>
                    <CardDescription>Areas of highest activity during the match</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="aspect-video bg-muted/20 rounded-lg border border-primary/20 flex items-center justify-center">
                      <div className="text-center space-y-2">
                        <Zap className="h-12 w-12 text-primary mx-auto animate-pulse" />
                        <p className="text-lg font-medium">Heatmap Visualization</p>
                        <p className="text-sm text-muted-foreground">
                          Interactive map showing player movement and engagement zones
                        </p>
                        <Badge variant="outline" className="mt-2">
                          Coming Soon
                        </Badge>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
