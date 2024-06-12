import { App } from "./App.tsx";
import { FirebaseAppProvider } from "reactfire";
import { firebaseConfig } from "./firebase.ts";
import * as React from "react";
import * as ReactDOM from "react-dom";

ReactDOM.render(
  <React.StrictMode>
    <FirebaseAppProvider firebaseConfig={firebaseConfig}>
      <App />
    </FirebaseAppProvider>
  </React.StrictMode>,
  document.getElementById("root"),
);
