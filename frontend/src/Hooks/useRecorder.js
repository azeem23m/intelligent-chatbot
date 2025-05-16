import { useState, useRef, useEffect } from "react";


  const  useAudioRecorder=()=> {

  const CHUNK_DURATION = 60 * 1000; 


  const [isRecording, setIsRecording] = useState(false);
  const [error, setError] = useState(null);
  const [chunksCount, setChunksCount] = useState(0);
  const [log, setLog] = useState([]); 


  const streamRef = useRef(null);
  const mediaRecorderRef = useRef(null);
  const accumulatedTimeRef = useRef(0);
  const recordingFlagRef = useRef(false); 


  const startRecording = async () => {
    if (recordingFlagRef.current) return; 

    try {
      const stream = await navigator.mediaDevices.getDisplayMedia({
        audio: true,
        video: true,
      });

      stream.getVideoTracks().forEach((t) => t.stop());
      stream.getTracks().forEach((t) => (t.onended = stopRecording));

      streamRef.current = stream;
      accumulatedTimeRef.current = 0;
      setChunksCount(0);
      setError(null);
      setLog([]); 

      recordingFlagRef.current = true;
      setIsRecording(true);

      recordChunk();
    } catch (err) {
      console.error("getDisplayMedia failed", err);
   
    }
  };

  const recordChunk = () => {
    if (!recordingFlagRef.current || !streamRef.current) return;

    const chunks = [];
    const mediaRecorder = new MediaRecorder(streamRef.current);
    mediaRecorderRef.current = mediaRecorder;

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data);
    };

    mediaRecorder.onstop = async () => {
      if (!chunks.length) return;

      const blob = new Blob(chunks, { type: "audio/webm" });
      const start = accumulatedTimeRef.current / 1000;
      const end = (accumulatedTimeRef.current + CHUNK_DURATION) / 1000;

      const body = new FormData();
      body.append("audio", blob);
      body.append("start_time", start);
      body.append("end_time", end);

 
      fetch("http://localhost:8000/data/audio-upload", { method: "POST", body });
    
      console.log(`✅ Uploaded ${start}s → ${end}s`);
      setChunksCount((c) => c + 1);


      accumulatedTimeRef.current += CHUNK_DURATION;

      if (recordingFlagRef.current) setTimeout(recordChunk, 0);
    };

    mediaRecorder.start();

    setTimeout(() => {
      if (mediaRecorder.state !== "inactive") mediaRecorder.stop();
    }, CHUNK_DURATION);
  };

  const stopRecording = () => {
    recordingFlagRef.current = false;
    setIsRecording(false);

    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
      mediaRecorderRef.current.stop();
    }

    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }

    setLog((prev) => [...prev, `🛑 Recording stopped at ${Math.floor(accumulatedTimeRef.current / 60)}:${(accumulatedTimeRef.current / 1000 % 60).toFixed(0).padStart(2, '0')}`]);
  };

  useEffect(() => {
    recordingFlagRef.current = isRecording;
  }, [isRecording]);

  useEffect(() => () => stopRecording(), []);

  return { startRecording, stopRecording, isRecording, error, chunksCount, log };
}
export{ useAudioRecorder };