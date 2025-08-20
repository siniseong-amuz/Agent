export function startTypingAnimation(text, onUpdate, onComplete, speed = 80, delay = 0) {
  let i = 0;
  let currentText = '';
  
  const typeInterval = setInterval(() => {
    if (i < text.length) {
      currentText += text[i];
      onUpdate(currentText);
      i++;
    } else {
      clearInterval(typeInterval);
      if (onComplete) {
        setTimeout(onComplete, 500);
      }
    }
  }, speed);
  
  if (delay > 0) {
    clearInterval(typeInterval);
    setTimeout(() => {
      startTypingAnimation(text, onUpdate, onComplete, speed, 0);
    }, delay);
  }
  
  return typeInterval;
}

export function stopTypingAnimation(intervalId) {
  if (intervalId) {
    clearInterval(intervalId);
  }
}
