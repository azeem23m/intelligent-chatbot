import { Textarea } from "../ui/textarea";
import { cx } from 'classix';
import { Button } from "../ui/button";
import { ArrowUpIcon } from "./icons"
import { toast } from 'sonner';
import { motion } from 'framer-motion';
import { useState } from 'react';
import { useAudioRecorder } from "../../Hooks/useRecorder";

const PlayIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M4 2L12 8L4 14V2Z" fill="currentColor" />
  </svg>
);

const StopIcon = () => (
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="4" y="4" width="8" height="8" fill="currentColor" />
  </svg>
);

interface ChatInputProps {
    question: string;
    setQuestion: (question: string) => void;
    onSubmit: (text?: string) => void;
    isLoading: boolean;
}

export const ChatInput = ({ question, setQuestion, onSubmit, isLoading }: ChatInputProps) => {
    const {
        startRecording,
        stopRecording,
        isRecording
    } = useAudioRecorder();

    return(
    <div className="relative w-full flex flex-col gap-4">
        <Textarea
        placeholder="Send a message..."
        className={cx(
            'min-h-[24px] max-h-[calc(75dvh)] overflow-hidden resize-none rounded-xl text-base bg-muted',
        )}
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyDown={(event) => {
            if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();

                if (isLoading) {
                    toast.error('Please wait for the model to finish its response!');
                } else {
                    onSubmit();
                }
            }
        }}
        rows={3}
        autoFocus
        />
    
    <div className="absolute bottom-2 left-2 flex gap-2">
        {isRecording ? (
            <Button
                className="rounded-full p-1.5 h-fit m-0.5 border dark:border-zinc-600 hover:bg-accent hover:text-accent-foreground"
                onClick={() => {
                    stopRecording();
                }}
            >
                <StopIcon />
            </Button>
        ):(
            <Button
                className="rounded-full p-1.5 h-fit m-0.5 border dark:border-zinc-600 hover:bg-accent hover:text-accent-foreground"
                onClick={() => startRecording()}
            >
                <PlayIcon />
            </Button>
        )}
    </div>
    <div className="absolute bottom-2 right-2">
        <Button
          className="rounded-full p-1.5 h-fit m-0.5 border dark:border-zinc-600 hover:bg-accent hover:text-accent-foreground"
          onClick={() => onSubmit(question)}
          disabled={question.length === 0}
        >
          <ArrowUpIcon size={14} />
        </Button>
    </div>
    </div>
    );
}









