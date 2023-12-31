import React, { useState } from "react";
import { Link } from 'react-router-dom';
import { useNavigate } from "react-router-dom";
import "../styles/LoginPage.css";
import API_URL from '../config';
import { ToastContainer, toast } from 'react-toastify';
const surfEmojiImage = require("../assets/surf-emoji.png");
const waveImage = require("../assets/wave.png");

interface User {
  userId: string;
  username: string;
}

interface LoginPageProps {
  setAuth: (token: string | null, user: User | null) => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ setAuth }) => {
  const [loginForm, setloginForm] = useState({
    userIdentifier: "",
    password: "",
  });

  const [errorMessages, setErrorMessages] = useState({
    userIdentifier: "",
    password: "",
    loginError: "",
  });

  const [isButtonDisabled, setIsButtonDisabled] = useState(false);

  const navigate = useNavigate();

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const { value, name } = event.target;
    setloginForm((prevForm) => ({
      ...prevForm,
      [name]: value,
    }));
  };

  const logMeIn = async (event: React.FormEvent) => {
    event.preventDefault();
    setErrorMessages({ userIdentifier: "", password: "", loginError: "" });
    const validateErrors = validate();
    if (validateErrors.userIdentifier || validateErrors.password) {
      setErrorMessages({
        userIdentifier: validateErrors.userIdentifier,
        password: validateErrors.password,
        loginError: "",
      });
      return;
    }

    try {
      setIsButtonDisabled(true);
      const response = await fetch(`${API_URL}/api/token`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_identifier: loginForm.userIdentifier,
          password: loginForm.password,
        }),
      });

      
      const data = await response.json();
      setIsButtonDisabled(false);
      if (!response.ok) {
        if (response.status === 401) {
          setErrorMessages({
            userIdentifier: "",
            password: "",
            loginError: "Invalid username or password",
          });
          throw new Error(data["error message"]);
        } else if (response.status === 404) {
          setErrorMessages({
            userIdentifier: "",
            password: "",
            loginError: "Invalid username or password",
          });
          throw new Error(data["error message"]);
        } else if (response.status === 500) {
          toast.error(`Oops, something went wrong. Please try again later!`, {
            position: toast.POSITION.TOP_CENTER,
          });
          throw new Error(data["error message"]);
        } else {
          toast.error(`Oops, something went wrong. Please try again later!`, {
            position: toast.POSITION.TOP_CENTER,
          });
          throw new Error("Network response was not ok.");
        }
      }

      setAuth(data.access_token, {userId: data.id, username: data.username});
      navigate("/");
      toast.success(`Welcome ${data.username}!`, {
        position: toast.POSITION.TOP_CENTER,
      });
    } catch (error: any) {
      console.error("Login Error:", error);
      setIsButtonDisabled(false);
    }

    setloginForm({
      userIdentifier: "",
      password: "",
    });
  };

  const validate = () => {
    const error = {
      userIdentifier: "",
      password: "",
    };

    if (!loginForm.userIdentifier) {
      error.userIdentifier = "Username or email is required";
    } else {
      error.userIdentifier = "";
    }

    if (!loginForm.password) {
      error.password = "Password is required";
    } else {
      error.password = "";
    }

    return error;
  };

  return (
    <div className="login-page-wrapper">
      <ToastContainer />
      <div className="row">
        <div className="col-md-4">
          <div className="image-container">
            <img src={surfEmojiImage} alt="..." className="surf-image" />
            <img src={waveImage} alt="..." className="wave-image" />
          </div>
        </div>
        <div className="col-md-8">
          <div className="login-container">
            <h1>Sign in to BlueSurf</h1>
            <p className="login-subtext">
              Get back to discovering UofT activities and events.
            </p>
            <form method="post" action="/">
              <div className="form-group userinput">
                <input
                  type="text"
                  id="username"
                  name="userIdentifier"
                  className="form-control input-boxes"
                  placeholder="Username/Email"
                  value={loginForm.userIdentifier}
                  onChange={handleChange}
                />
                {errorMessages.userIdentifier && (
                  <div className="error">{errorMessages.userIdentifier}</div>
                )}
              </div>
              <div className="form-group">
                <input
                  type="password"
                  id="password"
                  name="password"
                  className="form-control input-boxes"
                  placeholder="Password"
                  value={loginForm.password}
                  onChange={handleChange}
                />
                {errorMessages.password && (
                  <div className="error">{errorMessages.password}</div>
                )}
                {errorMessages.loginError && (
                  <div className="error">{errorMessages.loginError}</div>
                )}
              </div>
              <div className="form-group">
                <button type="submit" className="login-btn" onClick={logMeIn} disabled={isButtonDisabled}>
                  Login
                </button>
              </div>
            </form>
            <p className="login-subtext bottom-subtext">
              {" "}
              New to BlueSurf? <Link to="/register">Join Now</Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
