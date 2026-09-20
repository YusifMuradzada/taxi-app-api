import { useState } from "react";

function LoginModal({ onClose }: { onClose: () => void }) {
  const [register, setRegister] = useState(false);

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");

  const handleRegister = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            name: name,
            email: email,
            password: password,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(JSON.stringify(data.detail, null, 2));
        return;
      }

      alert("Account created successfully!");

      setRegister(false);
      setName("");
      setEmail("");
      setPassword("");
    } catch (error) {
      alert("Serverə qoşulmaq mümkün olmadı");
    }
  };

  const handleLogin = async () => {
    try {
      const response = await fetch(
        "http://127.0.0.1:8000/auth/login",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: loginEmail,
            password: loginPassword,
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        alert(JSON.stringify(data.detail, null, 2));
        return;
      }

      localStorage.setItem("token", data.access_token);

      alert("Login successful!");

      onClose();
    } catch (error) {
      alert("Serverə qoşulmaq mümkün olmadı");
    }
  };

  return (
    <div className="login-overlay">
      <div className="login-modal">

        <button
          className="close-button"
          onClick={onClose}
        >
          ×
        </button>

        {!register ? (
          <>
            <h2>Welcome back</h2>
            <p>Login to your TAXIGO account</p>

            <input
              type="email"
              placeholder="Email"
              value={loginEmail}
              onChange={(e) => setLoginEmail(e.target.value)}
            />

            <input
              type="password"
              placeholder="Password"
              value={loginPassword}
              onChange={(e) => setLoginPassword(e.target.value)}
            />

            <button
              className="login-submit"
              onClick={handleLogin}
            >
              Login
            </button>

            <p className="register-text">
              Don't have an account?{" "}
              <span onClick={() => setRegister(true)}>
                Sign up
              </span>
            </p>
          </>
        ) : (
          <>
            <h2>Create account</h2>
            <p>Join TAXIGO and start riding</p>

            <input
              type="text"
              placeholder="Name"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />

            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />

            <button
              className="login-submit"
              onClick={handleRegister}
            >
              Create account
            </button>

            <p className="register-text">
              Already have an account?{" "}
              <span onClick={() => setRegister(false)}>
                Login
              </span>
            </p>
          </>
        )}

      </div>
    </div>
  );
}

export default LoginModal;