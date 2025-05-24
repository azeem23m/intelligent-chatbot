import { Button } from "@/components/ui/button"
import { Copy, Check } from 'lucide-react'
import { useState } from "react"
import { message } from "../../interfaces/interfaces"

interface MessageActionsProps {
  message: message
}

export function MessageActions({ message }: MessageActionsProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = () => {
    navigator.clipboard.writeText(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="flex items-center space-x-1">
      <Button variant="ghost" size="icon" onClick={handleCopy}>
        {copied ? (
            <Check className="text-black dark:text-white" size={16} />
        ) : (
            <Copy className="text-gray-500" size={16} />
        )}
      </Button>
    </div>
  )
}