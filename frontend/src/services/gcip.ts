/// <reference types="vite/client" />

export const initGoogleAuth = (callback: (response: any) => void) => {
  // Assuming Google Identity Services script is loaded in index.html
  if (window.google?.accounts?.id) {
    window.google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: callback,
    });
    window.google.accounts.id.prompt(); // Prompt for one-tap
  } else {
    console.error("Google accounts script not loaded");
  }
};

export const renderGoogleButton = (elementId: string) => {
  if (window.google?.accounts?.id) {
    window.google.accounts.id.renderButton(
      document.getElementById(elementId)!,
      { theme: "outline", size: "large", width: 250 }
    );
  }
};
