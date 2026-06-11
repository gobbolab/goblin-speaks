document.addEventListener("DOMContentLoaded", () => {
    const codeBlocks = document.querySelectorAll("pre.highlight");
  
    codeBlocks.forEach((codeBlock) => {
      const copyButton = document.createElement("button");
      copyButton.className = "copy-code-btn";
      copyButton.type = "button";
      copyButton.innerText = "Copy";
  
      codeBlock.style.position = "relative";
      codeBlock.appendChild(copyButton);
  
      copyButton.addEventListener("click", async () => {
        const code = codeBlock.querySelector("code").innerText;
        await navigator.clipboard.writeText(code);
        
        copyButton.innerText = "Copied!";
        setTimeout(() => { copyButton.innerText = "Copy"; }, 2000);
      });
    });
  });