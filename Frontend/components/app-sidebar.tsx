"use client"

import { Gamepad2, Users, Mic, Shield, BarChart3, Settings, Cloud, Bell, MessageSquare } from "lucide-react"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarSeparator,
  SidebarTrigger,
} from "@/components/ui/sidebar"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { usePathname, useRouter } from "next/navigation"

export function AppSidebar() {
  const router = useRouter()
  const pathname = usePathname()

  const handleNavigation = (path: string) => {
    router.push(path)
  }

  return (
    <Sidebar variant="floating" collapsible="icon">
      <SidebarHeader className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <img src="/images/logo.png" alt="GhostLAN Logo" className="w-8 h-8" />
            <h1 className="text-xl font-bold text-primary glow-text">GhostLAN</h1>
          </div>
          <SidebarTrigger />
        </div>
      </SidebarHeader>

      <SidebarSeparator />

      <SidebarContent>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Matchmaking"
              isActive={pathname === "/" || pathname === "/matchmaking"}
              onClick={() => handleNavigation("/")}
            >
              <Gamepad2 className={pathname === "/" || pathname === "/matchmaking" ? "text-primary" : ""} />
              <span>Matchmaking</span>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Players"
              isActive={pathname === "/players"}
              onClick={() => handleNavigation("/players")}
            >
              <Users className={pathname === "/players" ? "text-primary" : ""} />
              <span>Players</span>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Voice Chat"
              isActive={pathname === "/voice-chat"}
              onClick={() => handleNavigation("/voice-chat")}
            >
              <Mic className={pathname === "/voice-chat" ? "text-primary" : ""} />
              <span>Voice Chat</span>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Anti-Cheat"
              isActive={pathname === "/anti-cheat"}
              onClick={() => handleNavigation("/anti-cheat")}
            >
              <Shield className={pathname === "/anti-cheat" ? "text-primary" : ""} />
              <span>Anti-Cheat</span>
              <Badge className="ml-auto bg-secondary text-xs">3</Badge>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Analytics"
              isActive={pathname === "/analytics"}
              onClick={() => handleNavigation("/analytics")}
            >
              <BarChart3 className={pathname === "/analytics" ? "text-primary" : ""} />
              <span>Analytics</span>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton tooltip="Chat" isActive={pathname === "/chat"} onClick={() => handleNavigation("/chat")}>
              <MessageSquare className={pathname === "/chat" ? "text-primary" : ""} />
              <span>Chat</span>
              <Badge className="ml-auto bg-primary text-xs">5</Badge>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>

        <SidebarSeparator className="my-2" />

        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Cloud Sync"
              isActive={pathname === "/cloud-sync"}
              onClick={() => handleNavigation("/cloud-sync")}
            >
              <Cloud className={pathname === "/cloud-sync" ? "text-primary" : ""} />
              <span>Cloud Sync</span>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Notifications"
              isActive={pathname === "/notifications"}
              onClick={() => handleNavigation("/notifications")}
            >
              <Bell className={pathname === "/notifications" ? "text-primary" : ""} />
              <span>Notifications</span>
              <Badge className="ml-auto bg-secondary text-xs">2</Badge>
            </SidebarMenuButton>
          </SidebarMenuItem>

          <SidebarMenuItem>
            <SidebarMenuButton
              tooltip="Settings"
              isActive={pathname === "/settings"}
              onClick={() => handleNavigation("/settings")}
            >
              <Settings className={pathname === "/settings" ? "text-primary" : ""} />
              <span>Settings</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarContent>

      <SidebarFooter className="p-6">
        <div className="flex items-center gap-3 p-2 rounded-lg hover:bg-muted/20 transition-all cursor-pointer">
          <Avatar className="border-2 border-primary glow-border">
            <AvatarImage src="/placeholder.svg?height=40&width=40" />
            <AvatarFallback className="bg-muted text-primary">GH</AvatarFallback>
          </Avatar>
          <div className="flex flex-col">
            <span className="text-sm font-medium">GhostPlayer</span>
            <span className="text-xs text-muted-foreground">Online</span>
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}
