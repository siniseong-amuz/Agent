export const parseAIResponse = (response) => {
  if (!response) return '';
  
  if (typeof response === 'object') {
    if (response.original && response.translation) {
      return { type: 'translation', original: response.original, translation: response.translation };
    }
    
    if (response.response) {
      return response.response;
    }
    
    return JSON.stringify(response, null, 2);
  }
  
  try {
    const parsed = JSON.parse(response);
    
    if (parsed.original && parsed.translation) {
      return { type: 'translation', original: parsed.original, translation: parsed.translation };
    }
    
    if (parsed.response) {
      return parsed.response;
    }
    
    return JSON.stringify(parsed, null, 2);
  } catch (error) {
    return response;
  }
};


