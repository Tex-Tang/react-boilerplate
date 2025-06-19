import { Editor } from "@monaco-editor/react";

export default function App() {
  return (
    <div className="flex bg-gray-100 w-full min-h-screen">
      <div className="ml-[300px] flex-1">
        <div className="max-w-5xl">
          <Editor
            height="30vh"
            className="w-full text-lg"
            defaultLanguage="python"
            defaultValue=""
          />
        </div>
      </div>
    </div>
  );
}
