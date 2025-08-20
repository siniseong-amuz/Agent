export const parseAIResponse = (response) => {
  if (!response) return '';
  
  if (typeof response === 'object') {
    if (response.original && response.translation) {
      return `원문: ${response.original}\n번역문: ${response.translation}`;
    }
    
    if (response.response) {
      return response.response;
    }
    
    return JSON.stringify(response, null, 2);
  }
  
  try {
    const parsed = JSON.parse(response);
    
    if (parsed.original && parsed.translation) {
      return `원문: ${parsed.original}\n번역문: ${parsed.translation}`;
    }
    
    if (parsed.response) {
      return parsed.response;
    }
    
    return JSON.stringify(parsed, null, 2);
  } catch (error) {
    return response;
  }
};


