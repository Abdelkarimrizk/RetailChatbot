import { useState, useEffect, useRef } from "react";
import { FaPaperclip } from "react-icons/fa";
import { IoIosSend, IoIosArrowDown } from "react-icons/io";
import { PiChatsCircle } from "react-icons/pi";
import { IoCloseOutline } from "react-icons/io5";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const ChatPopup = () => {
  const [open, setOpen] = useState(true);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([
    { role: "assistant", content: "How can I help you today?" },
  ]);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);
  const [image, setImage] = useState(null);
  const fileInputRef = useRef();

  const fileToBase64 = (file) =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onloadend = () => resolve(reader.result.split(",")[1]);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });

  // Scroll to bottom when new messages are added
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  // Scroll to bottom when chat is reopened
  useEffect(() => {
    if (open && messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "auto" });
    }
  }, [open]);

  // Send message to backend
  const handleSend = async (messageOverride = null) => {
    const finalMessage = messageOverride ?? input;
    if (!finalMessage.trim() && !image) return;

    const localImageUrl = image ? URL.createObjectURL(image) : null;

    const userMessage = {
      role: "user",
      content: finalMessage,
      ...(localImageUrl && { image: localImageUrl }),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    let imageBase64 = null;
    if (image) {
      imageBase64 = await fileToBase64(image);
    }
    setImage(null);

    // strip 'image' field before sending history to backend
    const payloadHistory = messages.map(({ role, content }) => ({
      role,
      content,
    }));

    try {
      const response = await axios.post("/api/chat", {
        message: finalMessage,
        image: imageBase64,
        history: payloadHistory,
      });

      const { reply } = response.data;

      setMessages((prev) => [...prev, { role: "assistant", content: reply }]);
    } catch (err) {
      console.error("API error:", err);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Sorry, something went wrong. Please try again.",
        },
      ]);
    }

    setIsTyping(false);
  };

  return (
    <div className="fixed bottom-4 right-4 left-4 mx-auto sm:left-auto z-50 flex flex-col items-end space-y-2 w-[385px] sm:w-[500px]">
      {/* Chat window */}
      {open && (
        <div className=" w-full h-[80vh]  rounded-xl bg-zinc-900 shadow-lg flex flex-col overflow-hidden">
          {/* Header */}
          <div className="px-4 py-3 border-b border-zinc-800 bg-zinc-900 text-center">
            <h2 className="text-white font-semibold text-sm">Iris</h2>
          </div>

          {/* Message area */}
          <div className="flex-1 px-4 py-3 space-y-2 overflow-y-auto">
            {messages.map((msg, idx) => (
              <div
                className={`rounded-lg text-sm max-w-[75%] w-fit break-words ${
                  msg.role === "user"
                    ? "bg-blue-600 text-white self-end ml-auto"
                    : "bg-zinc-800 text-white self-start mr-auto"
                } ${msg.content ? "px-3 py-2" : "p-0"}`}
              >
                {msg.image && (
                  <img
                    src={msg.image}
                    alt="sent"
                    className="mb-1 max-h-40 rounded-md object-contain border border-zinc-600"
                  />
                )}
                {msg.content && (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      p: ({ node, ...props }) => (
                        <p className="text-sm text-white" {...props} />
                      ),
                      li: ({ node, ...props }) => (
                        <li
                          className="mb-1 mt-1 list-disc ml-5 text-sm text-white"
                          {...props}
                        />
                      ),
                      ul: ({ node, ...props }) => (
                        <ul className="mb-1" {...props} />
                      ),
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                )}
              </div>
            ))}
            {isTyping && (
              <div className="text-xs text-gray-400 italic">
                Iris is typing...
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Suggested prompts */}
          <div className="px-4 pb-2 flex flex-wrap gap-2">
            {["What can you do?"].map((suggestion, i) => (
              <button
                key={i}
                onClick={() => handleSend(suggestion)}
                className="bg-zinc-800 text-white text-sm px-3 py-1 rounded-full hover:bg-zinc-700 border border-zinc-700"
              >
                {suggestion}
              </button>
            ))}
          </div>
          {/* Image preview */}
          {image && (
            <div className="relative px-4 pb-2 w-fit">
              <img
                src={URL.createObjectURL(image)}
                alt="preview"
                className="h-20 rounded-md object-contain border border-zinc-700"
              />
              <button
                onClick={() => setImage(null)}
                className="absolute top-1 right-5 bg-black/50 hover:bg-black/80 text-white rounded-full p-1"
                title="Remove image"
              >
                <IoCloseOutline size={14} />
              </button>
            </div>
          )}
          {/* Input bar */}
          <div className="flex items-center px-3 py-2 bg-zinc-900 border-t border-zinc-800">
            <FaPaperclip
              className="text-gray-400 mr-2 cursor-pointer"
              onClick={() => fileInputRef.current?.click()}
            />
            <input
              type="file"
              accept="image/*"
              className="hidden"
              ref={fileInputRef}
              onChange={(e) => {
                const file = e.target.files[0];
                if (file) {
                  if (file.size > 3 * 1024 * 1024) {
                    alert("Image size must be under 3MB");
                    return;
                  }
                  setImage(file);
                }
              }}
            />
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Write a message..."
              className="flex-1 bg-transparent text-white placeholder-gray-400 text-sm focus:outline-none"
            />
            <button
              onClick={() => handleSend()}
              className="ml-2 bg-blue-500 hover:bg-blue-600 p-2 rounded-md text-white"
            >
              <IoIosSend size={16} />
            </button>
          </div>
        </div>
      )}

      {/* Toggle Button */}
      <button
        onClick={() => setOpen(!open)}
        className="bg-blue-500 hover:bg-blue-600 text-white rounded-full w-10 h-10 flex items-center justify-center shadow-md"
      >
        {open ? <IoIosArrowDown size={20} /> : <PiChatsCircle size={20} />}
      </button>
      
    </div>
  );
};

export default ChatPopup;
