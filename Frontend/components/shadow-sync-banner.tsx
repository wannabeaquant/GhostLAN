"use client"

import { useState, useEffect } from "react"
import { Cloud, CloudOff, CheckCircle, AlertCircle } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"

export function ShadowSyncBanner() {
  const [syncStatus, setSyncStatus] = useState<"online" | "offline" | "syncing">("online")
  const [syncProgress, setSyncProgress] = useState(0)
  const [lastSync, setLastSync] = useState(new Date())
  const [queueCount, setQueueCount] = useState(3)

  // Simulate sync status changes
  useEffect(() => {
    const interval = setInterval(() => {
      const random = Math.random()
      if (random > 0.8) {
        setSyncStatus("syncing")
        setSyncProgress(0)

        // Simulate sync progress
        const progressInterval = setInterval(() => {
          setSyncProgress((prev) => {
            if (prev >= 100) {
              clearInterval(progressInterval)
              setSyncStatus("online")
              setLastSync(new Date())
              setQueueCount(Math.max(0, queueCount - 1))
              return 100
            }
            return prev + 10
          })
        }, 200)
      } else if (random < 0.1) {
        setSyncStatus("offline")
      } else {
        setSyncStatus("online")
      }
    }, 10000)

    return () => clearInterval(interval)
  }, [queueCount])

  const getStatusIcon = () => {
    switch (syncStatus) {
      case "online":
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case "offline":
        return <CloudOff className="h-4 w-4 text-destructive" />
      case "syncing":
        return <Cloud className="h-4 w-4 text-primary animate-pulse" />
      default:
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
    }
  }

  const getStatusText = () => {
    switch (syncStatus) {
      case "online":
        return "ShadowSync Online"
      case "offline":
        return "ShadowSync Offline"
      case "syncing":
        return "Syncing to Cloud..."
      default:
        return "ShadowSync Unknown"
    }
  }

  const getStatusColor = () => {
    switch (syncStatus) {
      case "online":
        return "border-green-500/30 text-green-500"
      case "offline":
        return "border-destructive/30 text-destructive"
      case "syncing":
        return "border-primary/30 text-primary"
      default:
        return "border-yellow-500/30 text-yellow-500"
    }
  }

  const formatLastSync = () => {
    const now = new Date()
    const diff = Math.floor((now.getTime() - lastSync.getTime()) / 1000)

    if (diff < 60) return `${diff}s ago`
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
    return `${Math.floor(diff / 3600)}h ago`
  }

  return (
    <TooltipProvider>
      <Tooltip>
        <TooltipTrigger asChild>
          <div className="flex items-center gap-3">
            <Badge variant="outline" className={`px-3 py-1.5 ${getStatusColor()}`}>
              {getStatusIcon()}
              <span className="ml-2 text-xs font-medium">{getStatusText()}</span>
            </Badge>

            {queueCount > 0 && syncStatus !== "syncing" && (
              <Badge variant="outline" className="px-2 py-1 text-xs">
                Queue: {queueCount}
              </Badge>
            )}
          </div>
        </TooltipTrigger>
        <TooltipContent side="bottom" className="max-w-xs">
          <div className="space-y-2 text-xs">
            <div className="flex justify-between">
              <span className="text-muted-foreground">Status:</span>
              <span className="capitalize">{syncStatus}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-muted-foreground">Last Sync:</span>
              <span>{formatLastSync()}</span>
            </div>
            {queueCount > 0 && (
              <div className="flex justify-between">
                <span className="text-muted-foreground">Queue:</span>
                <span>{queueCount} items pending</span>
              </div>
            )}
            {syncStatus === "syncing" && (
              <div className="space-y-1">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Progress:</span>
                  <span>{syncProgress}%</span>
                </div>
                <Progress value={syncProgress} className="h-1" />
              </div>
            )}
          </div>
        </TooltipContent>
      </Tooltip>
    </TooltipProvider>
  )
}
