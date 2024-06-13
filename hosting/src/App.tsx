import { connectAuthEmulator, getAuth } from "firebase/auth";
import {
  AuthProvider,
  FirestoreProvider,
  FunctionsProvider,
  StorageProvider,
  DatabaseProvider,
  useFirebaseApp,
} from "reactfire";
import { firebaseConfig } from "./firebase.ts";
import { initializeApp } from "firebase/app";
import { connectFunctionsEmulator, getFunctions } from "firebase/functions";
import { connectFirestoreEmulator, getFirestore } from "firebase/firestore";
import { connectStorageEmulator, getStorage } from "firebase/storage";
import { connectDatabaseEmulator, getDatabase } from "firebase/database";

import { Routing } from "./routes.tsx";
import { GameProvider } from "./hooks/GameProvider.tsx";

export const App = () => {
  const app = initializeApp(firebaseConfig);

  const auth = getAuth(useFirebaseApp());
  const functions = getFunctions(app);
  const firestore = getFirestore(app);
  const storage = getStorage(app);
  const database = getDatabase(app);

  functions.region = "europe-west1";

  const app_env: string | undefined = import.meta.env.VITE_API_APP_ENV;

  if (app_env === "development") {
    connectFunctionsEmulator(functions, "localhost", 5001);
    connectAuthEmulator(auth, "http://localhost:9099/");
    connectFirestoreEmulator(firestore, "localhost", 8080);
    connectStorageEmulator(storage, "localhost", 9199);
    connectDatabaseEmulator(database, "localhost", 9000);
  }

  return (
    // Firebase hooks
    <AuthProvider sdk={auth}>
      <FunctionsProvider sdk={functions}>
        <FirestoreProvider sdk={firestore}>
          <StorageProvider sdk={storage}>
            <DatabaseProvider sdk={database}>
              <GameProvider>
                <Routing />
              </GameProvider>
            </DatabaseProvider>
          </StorageProvider>
        </FirestoreProvider>
      </FunctionsProvider>
    </AuthProvider>
  );
};
