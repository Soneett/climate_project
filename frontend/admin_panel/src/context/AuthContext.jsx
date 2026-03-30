import React, { createContext, useContext, useState } from "react";
import { MOCK_USERS } from "../data/mockData";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [error, setError] = useState("");

  function login(email, password) {
    const user = MOCK_USERS.find(
      (u) => u.email === email && u.password === password
    );
    if (user) {
      setCurrentUser(user);
      setError("");
      return true;
    }
    setError("Неверный email или пароль");
    return false;
  }

  function logout() {
    setCurrentUser(null);
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
