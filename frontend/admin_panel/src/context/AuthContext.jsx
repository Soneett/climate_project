import React, { createContext, useContext, useState } from "react";
import { MOCK_USERS } from "../data/mockData";

const AuthContext = createContext(null);
const STORAGE_KEY = "admin_panel_current_user";

function getStoredUser() {
  if (typeof window === "undefined") {
    return null;
  }

  const storedValue = window.localStorage.getItem(STORAGE_KEY);
  if (!storedValue) {
    return null;
  }

  try {
    const parsed = JSON.parse(storedValue);
    if (!parsed?.id) {
      return null;
    }

    const userFromMock = MOCK_USERS.find((user) => user.id === parsed.id);
    return userFromMock ?? null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(() => getStoredUser());
  const [error, setError] = useState("");

  function login(email, password) {
    const user = MOCK_USERS.find(
      (u) => u.email === email && u.password === password
    );
    if (user) {
      setCurrentUser(user);
      if (typeof window !== "undefined") {
        window.localStorage.setItem(STORAGE_KEY, JSON.stringify({ id: user.id }));
      }
      setError("");
      return true;
    }
    setError("Неверный email или пароль");
    return false;
  }

  function logout() {
    setCurrentUser(null);
    if (typeof window !== "undefined") {
      window.localStorage.removeItem(STORAGE_KEY);
    }
    setError("");
  }

  return (
    <AuthContext.Provider value={{ currentUser, login, logout, error }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
