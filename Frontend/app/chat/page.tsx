"use client"

import { useState, useRef, useEffect } from "react"
import { SidebarProvider } from "@/components/ui/sidebar"
import { AppSidebar } from "@/components/app-sidebar"
import { ShadowSyncBanner } from "@/components/shadow-sync-banner"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { User, Users } from "lucide-react"

// Mock chat data
const CHAT_CHANNELS = [
  { id: 1, name: "General", unread: 0, isActive: true },
  { id: 2, name: "Team Alpha", unread: 3, isActive: false },
  { id: 3, name: "Team Beta", unread: 0, isActive: false },
  { id: 4, name: "Tournament", unread: 5, isActive: false },
  { id: 5, name: "Tech Support", unread: 0, isActive: false },
]

const DIRECT_MESSAGES = [
  { id: 1, name: "CyberNinja", status: "online", avatar: "/placeholder.svg?height=40&width=40", unread: 2 },
  { id: 2, name: "QuantumFrag", status: "online", avatar: "/placeholder.svg?height=40&width=40", unread: 0 },
  { id: 3, name: "NeonSniper", status: "in-game", avatar: "/placeholder.svg?height=40&width=40", unread: 0 },
  { id: 4, name: "ShadowByte", status: "online", avatar: "/placeholder.svg?height=40&width=40", unread: 0 },
]

const MESSAGES = [
  {
    id: 1,
    sender: "CyberNinja",
    avatar: "/placeholder.svg?height=40&width=40",
    content: "Hey everyone! Who's up for a practice match tonight?",
    timestamp: "10:15 AM",
    isOwn: false,
  },
  {
    id: 2,
    sender: "QuantumFrag",
    avatar: "/placeholder.svg?height=40&width=40",
    content: "I'm in! What time were you thinking?",
    timestamp: "10:17 AM",
    isOwn: false,
  },
  {
    id: 3,
    sender: "GhostPlayer",
    avatar: "/placeholder.svg?height=40&width=40",
    content: "Count me in too. I'm free after 8PM.",
    timestamp: "10:20 AM",
    isOwn: true,
  },
  {
    id: 4,
    sender: "NeonSniper",
    avatar: "/placeholder.svg?height=40&width=40",
    content: "Perfect! Let's do 8:30PM then. I'll set up the server.",
    timestamp: "10:22 AM",
    isOwn: false,
  },
  {
    id: 5,
    sender: "ShadowByte",
    avatar: "/placeholder.svg?height=40&width=40",
    content: "Anyone want to test the new map before the match? I heard they added some interesting hiding spots.",
    timestamp: "10:25 AM",
    isOwn: false,
  },
  {
    id: 6,
    sender: "GhostPlayer",
    avatar: "/placeholder.svg?height=40&width=40",
    content: "I'm down to check out the new map. Should we meet 30 minutes earlier?",
    timestamp: "10:28 AM",
    isOwn: true,
  },
  {
    id: 7,
    sender: "CyberNinja",
    avatar: "/placeholder.svg?height=40&width=40",
    content: "Sounds good to me! 8PM for map exploration, 8:30PM for the match.",
    timestamp: "10:30 AM",
    isOwn: false,
  },
]

export default function ChatPage() {
  const [message, setMessage] = useState("")
  const [messages, setMessages] = useState(MESSAGES)
  const [activeChannel, setActiveChannel] = useState("General")
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSendMessage = () => {
    if (message.trim() === "") return

    const newMessage = {
      id: messages.length + 1,
      sender: "GhostPlayer",
      avatar: "/placeholder.svg?height=40&width=40",
      content: message,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      isOwn: true,
    }

    setMessages([...messages, newMessage])
    setMessage("")
  }

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

            <div className="flex-1 flex overflow-hidden">
              {/* Chat Sidebar */}
              <div className="w-64 border-r border-border/40 bg-background/60 backdrop-blur-sm flex flex-col overflow-hidden">
                <div className="p-4 border-b border-border/40">
                  <h2 className="text-lg font-medium">Chat</h2>
                </div>
                
                <div className="flex-1 overflow-y-auto">
                  <div className="p-4">
                    <h3 className="text-xs uppercase text-muted-foreground font-medium mb-2 flex items-center gap-2">
                      <Users className="h-3 w-3" /> Channels
                    </h3>
                    <div className="space-y-1">
                      {CHAT_CHANNELS.map((channel) => (
                        <button
                          key={channel.id}
                          className={`w-full flex items-center justify-between p-2 rounded-md text-sm hover:bg-muted/50 transition-colors ${
                            channel.isActive ? "bg-primary/10 text-primary" : ""
                          }`}
                          onClick={() => setActiveChannel(channel.name)}
                        >
                          <span># {channel.name}</span>
                          {channel.unread > 0 && (
                            <span className="bg-primary text-primary-foreground text-xs rounded-full h-5 w-5 flex items-center justify-center">
                              {channel.unread}
                            </span>
                          )}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="p-4">
                    <h3 className="text-xs uppercase text-muted-foreground font-medium mb-2 flex items-center gap-2">
                      <User className="h-3 w-3" /> Direct Messages
                    </h3>
                    <div className="space-y-1">
                      {DIRECT_MESSAGES.map((dm) => (
                        <button
                          key={dm.id}
                          className="w-full flex items-center justify-between p-2 rounded-md text-sm hover:bg-muted/50 transition-colors"
                          onClick={() => setActiveChannel(dm.name)}
                        >
                          <div className="flex items-center gap-2">
                            <div className="relative">
                              <Avatar className="h-6 w-6">
                                <AvatarImage src={dm.avatar || "/placeholder.svg"} />
                                <AvatarFallback>{dm.name.substring(0, 2)}</AvatarFallback>
                              </Avatar>
                              <span
                                className={`absolute -bottom-0.5 -right-0.5 h-2 w-2 ${getStatusColor(
                                  dm.status
                                )} rounded-full border border-background`}
                              ></span>
                            </div>
                            <span>{dm.name}</span>
                          </div>
                          {dm.unread > 0 && (
                            <span className="bg-primary text-primary-foreground text-xs rounded-full h-5 w-5 flex items-center justify-center">
                              {dm.unread}
                            </span>
                          )}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>

              {/* Chat Content */}
              <div className="flex-1 flex flex-col overflow-hidden">
                <div className="p-4 border-b border-border/40 bg-background/40 backdrop-blur-sm">
                  <h2 className="text-lg font-medium">#{activeChannel}</h2>
                </div>

                <div className="flex-1 overflow-y-auto p-4">
                  <div className="space-y-4">
                    {messages.map((msg) => (
                      <div
                        key={msg.id}
                        className={`flex gap-3 ${msg.isOwn ? "justify-end" : "justify-start"}`}
                      >
                        {!msg.isOwn && (
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={msg.avatar || "/placeholder.svg"} />
                            <AvatarFallback>{msg.sender.substring(0, 2)}</AvatarFallback>
                          </Avatar>
                        )}
                        <div
                          className={`max-w-[80%] rounded-lg p-3 ${
                            msg.isOwn
                              ? "bg-primary/20 text-primary-foreground"
                              : "bg-muted/50 text-foreground"
                          }`}
                        >
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-medium text-sm">{msg.sender}</span>
                            <span className="text-xs text-muted-foreground">{msg.timestamp}</span>
                          </div>
                          <p>{msg.content}</p>
                        </div>
                        {msg.isOwn && (
                          <Avatar className="h-8 w-8">
                            <AvatarImage src={msg.avatar || "/placeholder.svg"} />
                            <AvatarFallback>{msg.sender.substring(0, 2)}</AvatarFallback>
                          </Avatar>
                        )}
                      </div>
                    ))}
                    <div ref={messagesEndRef} />
                  </div>
