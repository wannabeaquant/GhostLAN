"use client"

import { useState } from "react"
import { Shield, AlertTriangle, AlertCircle, Info, Search, Filter, RefreshCw } from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

// Mock anti-cheat events
const ANTI_CHEAT_EVENTS = [
  {
    id: 1,
    player: "ShadowByte",
    event: "Abnormal Reflex Detected",
    timestamp: "2025-06-12T20:15:32",
    severity: "high",
    details: "Reaction time consistently below human threshold (40ms) in last 5 encounters.",
  },
  {
    id: 2,
    player: "NeonSniper",
    event: "Suspicious Aim Pattern",
    timestamp: "2025-06-12T20:12:18",
    severity: "medium",
    details: "Tracking through walls detected in sector B-7.",
  },
  {
    id: 3,
    player: "QuantumFrag",
    event: "Memory Modification",
    timestamp: "2025-06-12T20:08:45",
    severity: "high",
    details: "Attempted to modify game memory at address 0x7FFE4321.",
  },
  {
    id: 4,
    player: "CyberNinja",
    event: "Network Packet Manipulation",
    timestamp: "2025-06-12T20:05:22",
    severity: "medium",
    details: "Irregular packet timing detected, possible speed hack.",
  },
  {
    id: 5,
    player: "VirtualPhantom",
    event: "System File Integrity",
    timestamp: "2025-06-12T20:01:10",
    severity: "low",
    details: "Modified system file detected, but not affecting gameplay.",
  },
  {
    id: 6,
    player: "ShadowByte",
    event: "Input Automation",
    timestamp: "2025-06-12T19:58:33",
    severity: "medium",
    details: "Macro usage suspected for rapid weapon switching.",
  },
  {
    id: 7,
    player: "NeonSniper",
    event: "Abnormal Movement",
    timestamp: "2025-06-12T19:55:17",
    severity: "low",
    details: "Unusual bunny-hop pattern detected, possible script.",
  },
]

export function AntiCheatPanel() {
  const [searchTerm, setSearchTerm] = useState("")
  const [severityFilter, setSeverityFilter] = useState("all")
  const [activeTab, setActiveTab] = useState("events")
  const [isScanning, setIsScanning] = useState(false)

  // Filter events based on search term and severity
  const filteredEvents = ANTI_CHEAT_EVENTS.filter((event) => {
    const matchesSearch =
      event.player.toLowerCase().includes(searchTerm.toLowerCase()) ||
      event.event.toLowerCase().includes(searchTerm.toLowerCase())

    const matchesSeverity = severityFilter === "all" || event.severity === severityFilter

    return matchesSearch && matchesSeverity
  })

  const handleScan = () => {
    setIsScanning(true)
    setTimeout(() => {
      setIsScanning(false)
    }, 2500)
  }

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case "high":
        return "bg-destructive text-destructive-foreground"
      case "medium":
        return "bg-yellow-500 text-black"
      case "low":
        return "bg-blue-500 text-white"
      default:
        return "bg-muted text-muted-foreground"
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case "high":
        return <AlertTriangle className="h-4 w-4" />
      case "medium":
        return <AlertCircle className="h-4 w-4" />
      case "low":
        return <Info className="h-4 w-4" />
      default:
        return <Info className="h-4 w-4" />
    }
  }

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp)
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" })
  }

  return (
    <div className="h-full p-8 overflow-auto grid-bg">
      <div className="max-w-6xl mx-auto space-y-8">
        <div className="flex flex-col md:flex-row gap-6">
          {/* Anti-Cheat Status */}
          <Card className="cyberpunk-card flex-1">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-xl flex items-center gap-2">
                  <Shield className="h-5 w-5 text-primary" />
                  Anti-Cheat Status
                </CardTitle>
                <Badge variant="outline" className="border-green-500 text-green-500 px-3 py-1">
                  ACTIVE
                </Badge>
              </div>
              <CardDescription>Real-time cheat detection system</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-muted/50 p-3 rounded-md">
                  <p className="text-xs text-muted-foreground">Engine Version</p>
                  <p className="font-medium">GhostGuard v4.2.1</p>
                </div>
                <div className="bg-muted/50 p-3 rounded-md">
                  <p className="text-xs text-muted-foreground">Definitions</p>
                  <p className="font-medium">Updated 12 minutes ago</p>
                </div>
                <div className="bg-muted/50 p-3 rounded-md">
                  <p className="text-xs text-muted-foreground">Scan Mode</p>
                  <p className="font-medium">Deep + Heuristic</p>
                </div>
              </div>

              <div className="flex flex-col sm:flex-row gap-3">
                <Button onClick={handleScan} disabled={isScanning} className="flex-1">
                  {isScanning ? (
                    <>
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                      Scanning...
                    </>
                  ) : (
                    <>
                      <Shield className="mr-2 h-4 w-4" />
                      Run Manual Scan
                    </>
                  )}
                </Button>
                <Button variant="outline" className="flex-1">
                  View Protection Details
                </Button>
              </div>
            </CardContent>
          </Card>

          {/* Stats Summary */}
          <Card className="cyberpunk-card w-full md:w-80">
            <CardHeader>
              <CardTitle className="text-xl">Detection Summary</CardTitle>
              <CardDescription>Last 24 hours</CardDescription>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="grid grid-cols-2 gap-6">
                <div className="bg-destructive/10 p-3 rounded-md border border-destructive/30">
                  <p className="text-xs text-muted-foreground">High Severity</p>
                  <p className="text-xl font-bold text-destructive">2</p>
                </div>
                <div className="bg-yellow-500/10 p-3 rounded-md border border-yellow-500/30">
                  <p className="text-xs text-muted-foreground">Medium Severity</p>
                  <p className="text-xl font-bold text-yellow-500">3</p>
                </div>
                <div className="bg-blue-500/10 p-3 rounded-md border border-blue-500/30">
                  <p className="text-xs text-muted-foreground">Low Severity</p>
                  <p className="text-xl font-bold text-blue-500">2</p>
                </div>
                <div className="bg-green-500/10 p-3 rounded-md border border-green-500/30">
                  <p className="text-xs text-muted-foreground">Players Banned</p>
                  <p className="text-xl font-bold text-green-500">1</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Event Log */}
        <Card className="cyberpunk-card">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-xl">Anti-Cheat Alerts</CardTitle>
              <Badge variant="outline" className="px-3 py-1">
                {filteredEvents.length} Events
              </Badge>
            </div>
            <CardDescription>Detected suspicious activities and violations</CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-4">
              <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
                <TabsList>
                  <TabsTrigger value="events" className="data-[state=active]:text-primary">
                    Events
                  </TabsTrigger>
                  <TabsTrigger value="players" className="data-[state=active]:text-primary">
                    Players
                  </TabsTrigger>
                  <TabsTrigger value="settings" className="data-[state=active]:text-primary">
                    Settings
                  </TabsTrigger>
                </TabsList>

                <div className="flex flex-col sm:flex-row w-full sm:w-auto gap-2">
                  <div className="relative flex-1">
                    <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Search events..."
                      className="pl-9"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </div>
                  <Select value={severityFilter} onValueChange={setSeverityFilter}>
                    <SelectTrigger className="w-full sm:w-[180px]">
                      <Filter className="mr-2 h-4 w-4" />
                      <SelectValue placeholder="Filter by severity" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">All Severities</SelectItem>
                      <SelectItem value="high">High Severity</SelectItem>
                      <SelectItem value="medium">Medium Severity</SelectItem>
                      <SelectItem value="low">Low Severity</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <TabsContent value="events" className="m-0">
                <div className="rounded-md border">
                  <div className="relative w-full overflow-auto">
                    <table className="w-full caption-bottom text-sm">
                      <thead className="[&_tr]:border-b">
                        <tr className="border-b transition-colors hover:bg-muted/50 data-[state=selected]:bg-muted">
                          <th className="h-10 px-4 text-left align-middle font-medium text-muted-foreground">
                            Severity
                          </th>
                          <th className="h-10 px-4 text-left align-middle font-medium text-muted-foreground">Player</th>
                          <th className="h-10 px-4 text-left align-middle font-medium text-muted-foreground">Event</th>
                          <th className="h-10 px-4 text-left align-middle font-medium text-muted-foreground">Time</th>
                          <th className="h-10 px-4 text-left align-middle font-medium text-muted-foreground">
                            Actions
                          </th>
                        </tr>
                      </thead>
                      <tbody className="[&_tr:last-child]:border-0">
                        {filteredEvents.map((event) => (
                          <tr
                            key={event.id}
                            className="border-b transition-all hover:bg-muted/20 hover:backdrop-blur-sm data-[state=selected]:bg-muted cursor-pointer"
                          >
                            <td className="p-4 align-middle">
                              <TooltipProvider>
                                <Tooltip>
                                  <TooltipTrigger asChild>
                                    <Badge className={`${getSeverityColor(event.severity)}`}>
                                      {getSeverityIcon(event.severity)}
                                      <span className="ml-1 capitalize">{event.severity}</span>
                                    </Badge>
                                  </TooltipTrigger>
                                  <TooltipContent>
                                    <p className="text-xs">{event.details}</p>
                                  </TooltipContent>
                                </Tooltip>
                              </TooltipProvider>
                            </td>
                            <td className="p-4 align-middle font-medium">{event.player}</td>
                            <td className="p-4 align-middle">{event.event}</td>
                            <td className="p-4 align-middle text-muted-foreground">
                              {formatTimestamp(event.timestamp)}
                            </td>
                            <td className="p-4 align-middle">
                              <div className="flex items-center gap-2">
                                <Button variant="ghost" size="sm">
                                  Details
                                </Button>
                                <Button variant="destructive" size="sm">
                                  Ban
                                </Button>
                              </div>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              </TabsContent>

              <TabsContent value="players" className="m-0">
                <div className="rounded-md border p-8 text-center">
                  <p className="text-muted-foreground">Player analysis view coming soon</p>
                </div>
              </TabsContent>

              <TabsContent value="settings" className="m-0">
                <div className="rounded-md border p-8 text-center">
                  <p className="text-muted-foreground">Anti-cheat settings view coming soon</p>
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
