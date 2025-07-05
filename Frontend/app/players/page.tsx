"use client"

import { useState } from "react"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { VoiceChatOverlay } from "@/components/voice-chat-overlay"
import { ShadowSyncBanner } from "@/components/shadow-sync-banner"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Search, UserPlus, Star, Clock, Gamepad2 } from "lucide-react"

// Mock player data
const PLAYERS = [
  {
    id: 1,
    name: "CyberNinja",
    status: "online",
    avatar: "/placeholder.svg?height=40&width=40",
    rank: "Diamond",
    level: 42,
    lastSeen: "Now",
    isFriend: true,
    isFavorite: true,
  },
  {
    id: 2,
    name: "QuantumFrag",
    status: "online",
    avatar: "/placeholder.svg?height=40&width=40",
    rank: "Platinum",
    level: 38,
    lastSeen: "Now",
    isFriend: true,
    isFavorite: false,
  },
  {
    id: 3,
    name: "NeonSniper",
    status: "in-game",
    avatar: "/placeholder.svg?height=40&width=40",
    rank: "Gold",
    level: 27,
    lastSeen: "5 min ago",
    isFriend: true,
    isFavorite: false,
  },
  {
    id: 4,
    name: "ShadowByte",
    status: "online",
    avatar: "/placeholder.svg?height=40&width=40",
    rank: "Diamond",
    level: 51,
    lastSeen: "Now",
    isFriend: false,
    isFavorite: false,
  },
  {
    id: 5,
    name: "VirtualPhantom",
    status: "offline",
    avatar: "/placeholder.svg?height=40&width=40",
    rank: "Platinum",
    level: 35,
    lastSeen: "3 hours ago",
    isFriend: true,
    isFavorite: true,
  },
  {
    id: 6,
    name: "LaserWolf",
    status: "in-game",
    avatar: "/placeholder.svg?height=40&width=40",
    rank: "Master",
    level: 67,
    lastSeen: "2 min ago",
    isFriend: false,
    isFavorite: false,
  },
  {
    id: 7,
    name: "PixelHunter",
    status: "online",
    avatar: "/placeholder.svg?height=40&width=40",
    rank: "Gold",
    level: 29,
    lastSeen: "Now",
    isFriend: false,
    isFavorite: false,
  },
  {
    id: 8,
    name: "BinaryBlade",
    status: "offline",
    avatar: "/placeholder.svg?height=40&width=40",
    rank: "Silver",
    level: 22,
    lastSeen: "1 day ago",
    isFriend: true,
    isFavorite: false,
  },
]

export default function PlayersPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [statusFilter, setStatusFilter] = useState("all")
  const [activeTab, setActiveTab] = useState("all")

  // Filter players based on search term and status
  const filteredPlayers = PLAYERS.filter((player) => {
    const matchesSearch = player.name.toLowerCase().includes(searchTerm.toLowerCase())
    const matchesStatus = statusFilter === "all" || player.status === statusFilter
    const matchesTab =
      activeTab === "all" ||
      (activeTab === "friends" && player.isFriend) ||
      (activeTab === "favorites" && player.isFavorite)

    return matchesSearch && matchesStatus && matchesTab
  })

  const getStatusColor = (status: string) => {
    switch (status) {
      case "online":
        return "bg-green-500"
      case "in-game":
        return "bg-blue-500"
      case "offline":
        return "bg-gray-500"
      default:
        return "bg-gray-500"
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case "online":
        return "Online"
      case "in-game":
        return "In Game"
      case "offline":
        return "Offline"
      default:
        return "Unknown"
    }
  }

  const getRankColor = (rank: string) => {
    switch (rank) {
      case "Master":
        return "text-purple-400 border-purple-400/30"
      case "Diamond":
        return "text-cyan-400 border-cyan-400/30"
      case "Platinum":
        return "text-blue-400 border-blue-400/30"
      case "Gold":
        return "text-yellow-400 border-yellow-400/30"
      case "Silver":
        return "text-gray-400 border-gray-400/30"
      default:
        return "text-gray-400 border-gray-400/30"
    }
  }

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

            <div className="h-full p-4 md:p-8 overflow-auto grid-bg">
              <div className="max-w-6xl mx-auto space-y-6">
                <Card className="cyberpunk-card">
                  <CardHeader>
                    <div className="flex items-center justify-between">
                      <CardTitle className="text-xl">Players</CardTitle>
                      <Badge variant="outline" className="px-3 py-1">
                        {filteredPlayers.length} Found
                      </Badge>
                    </div>
                    <CardDescription>Browse and connect with other players</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
                      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
                        <TabsList>
                          <TabsTrigger value="all" className="data-[state=active]:text-primary">
                            All Players
                          </TabsTrigger>
                          <TabsTrigger value="friends" className="data-[state=active]:text-primary">
                            Friends
                          </TabsTrigger>
                          <TabsTrigger value="favorites" className="data-[state=active]:text-primary">
                            Favorites
                          </TabsTrigger>
                        </TabsList>

                        <div className="flex flex-col sm:flex-row w-full sm:w-auto gap-2">
                          <div className="relative flex-1">
                            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                            <Input
                              placeholder="Search players..."
                              className="pl-9"
                              value={searchTerm}
                              onChange={(e) => setSearchTerm(e.target.value)}
                            />
                          </div>
                          <select
                            className="bg-muted/50 border border-border rounded-md p-2 h-10"
                            value={statusFilter}
                            onChange={(e) => setStatusFilter(e.target.value)}
                          >
                            <option value="all">All Statuses</option>
                            <option value="online">Online</option>
                            <option value="in-game">In Game</option>
                            <option value="offline">Offline</option>
                          </select>
                        </div>
                      </div>

                      <TabsContent value="all" className="m-0">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {filteredPlayers.map((player) => (
                            <div key={player.id} className="cyberpunk-card p-4 hover-lift cursor-pointer">
                              <div className="flex items-center gap-3">
                                <div className="relative">
                                  <Avatar className="h-12 w-12 border-2 border-primary/30">
                                    <AvatarImage src={player.avatar || "/placeholder.svg"} />
                                    <AvatarFallback>{player.name.substring(0, 2)}</AvatarFallback>
                                  </Avatar>
                                  <span
                                    className={`absolute -bottom-1 -right-1 h-3 w-3 ${getStatusColor(player.status)} rounded-full border-2 border-background`}
                                  ></span>
                                </div>
                                <div className="flex-1">
                                  <div className="flex items-center gap-2">
                                    <p className="font-medium">{player.name}</p>
                                    {player.isFavorite && <Star className="h-4 w-4 text-yellow-400 fill-yellow-400" />}
                                  </div>
                                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                    <span>{getStatusText(player.status)}</span>
                                    <span>•</span>
                                    <span>Lvl {player.level}</span>
                                  </div>
                                </div>
                                <Badge variant="outline" className={`${getRankColor(player.rank)}`}>
                                  {player.rank}
                                </Badge>
                              </div>
                              <div className="mt-3 flex items-center justify-between">
                                <div className="flex items-center gap-2 text-xs">
                                  <Clock className="h-3 w-3 text-muted-foreground" />
                                  <span className="text-muted-foreground">{player.lastSeen}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                  {player.isFriend ? (
                                    <Button variant="outline" size="sm">
                                      <Gamepad2 className="mr-1 h-3 w-3" />
                                      Invite
                                    </Button>
                                  ) : (
                                    <Button variant="outline" size="sm">
                                      <UserPlus className="mr-1 h-3 w-3" />
                                      Add
                                    </Button>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </TabsContent>

                      <TabsContent value="friends" className="m-0">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {filteredPlayers.map((player) => (
                            <div key={player.id} className="cyberpunk-card p-4 hover-lift cursor-pointer">
                              <div className="flex items-center gap-3">
                                <div className="relative">
                                  <Avatar className="h-12 w-12 border-2 border-primary/30">
                                    <AvatarImage src={player.avatar || "/placeholder.svg"} />
                                    <AvatarFallback>{player.name.substring(0, 2)}</AvatarFallback>
                                  </Avatar>
                                  <span
                                    className={`absolute -bottom-1 -right-1 h-3 w-3 ${getStatusColor(player.status)} rounded-full border-2 border-background`}
                                  ></span>
                                </div>
                                <div className="flex-1">
                                  <div className="flex items-center gap-2">
                                    <p className="font-medium">{player.name}</p>
                                    {player.isFavorite && <Star className="h-4 w-4 text-yellow-400 fill-yellow-400" />}
                                  </div>
                                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                    <span>{getStatusText(player.status)}</span>
                                    <span>•</span>
                                    <span>Lvl {player.level}</span>
                                  </div>
                                </div>
                                <Badge variant="outline" className={`${getRankColor(player.rank)}`}>
                                  {player.rank}
                                </Badge>
                              </div>
                              <div className="mt-3 flex items-center justify-between">
                                <div className="flex items-center gap-2 text-xs">
                                  <Clock className="h-3 w-3 text-muted-foreground" />
                                  <span className="text-muted-foreground">{player.lastSeen}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                  <Button variant="outline" size="sm">
                                    <Gamepad2 className="mr-1 h-3 w-3" />
                                    Invite
                                  </Button>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </TabsContent>

                      <TabsContent value="favorites" className="m-0">
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                          {filteredPlayers.map((player) => (
                            <div key={player.id} className="cyberpunk-card p-4 hover-lift cursor-pointer">
                              <div className="flex items-center gap-3">
                                <div className="relative">
                                  <Avatar className="h-12 w-12 border-2 border-primary/30">
                                    <AvatarImage src={player.avatar || "/placeholder.svg"} />
                                    <AvatarFallback>{player.name.substring(0, 2)}</AvatarFallback>
                                  </Avatar>
                                  <span
                                    className={`absolute -bottom-1 -right-1 h-3 w-3 ${getStatusColor(player.status)} rounded-full border-2 border-background`}
                                  ></span>
                                </div>
                                <div className="flex-1">
                                  <div className="flex items-center gap-2">
                                    <p className="font-medium">{player.name}</p>
                                    <Star className="h-4 w-4 text-yellow-400 fill-yellow-400" />
                                  </div>
                                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                                    <span>{getStatusText(player.status)}</span>
                                    <span>•</span>
                                    <span>Lvl {player.level}</span>
                                  </div>
                                </div>
                                <Badge variant="outline" className={`${getRankColor(player.rank)}`}>
                                  {player.rank}
                                </Badge>
                              </div>
                              <div className="mt-3 flex items-center justify-between">
                                <div className="flex items-center gap-2 text-xs">
                                  <Clock className="h-3 w-3 text-muted-foreground" />
                                  <span className="text-muted-foreground">{player.lastSeen}</span>
                                </div>
                                <div className="flex items-center gap-2">
                                  {player.isFriend ? (
                                    <Button variant="outline" size="sm">
                                      <Gamepad2 className="mr-1 h-3 w-3" />
                                      Invite
                                    </Button>
                                  ) : (
                                    <Button variant="outline" size="sm">
                                      <UserPlus className="mr-1 h-3 w-3" />
                                      Add
                                    </Button>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </TabsContent>
                    </Tabs>
                  </CardContent>
                </Card>
              </div>
            </div>
          </div>

          <VoiceChatOverlay />
        </div>
      </SidebarProvider>
    </main>
  )
}
