import React, { Component } from "react";
import axios from "axios";
import { Route, Routes } from "react-router-dom";

import NavBar from "./components/NavBar";
import LoginForm from "./components/LoginForm";
import UserStatus from "./components/UserStatus";
import CarriersList from "./components/CarriersList";

class App extends Component {
  constructor() {
    super();

    this.state = {
      users: [],
      trucks: [],
      title: "Genlogs Platform",
      accessToken: null,
    };
  }

  isAuthenticated = () => {
    if (this.state.accessToken || this.validRefresh()) {
      return true;
    }
    return false;
  };

  componentDidMount = () => {
    this.getCarriers();
  };

  validRefresh() {
    const token = window.localStorage.getItem("refreshToken");
    if (token) {
      axios
        .post(`${process.env.REACT_APP_API_SERVICE_URL}/auth/refresh`, {
          refresh_token: token,
        })
        .then((res) => {
          this.getCarriers();
          this.setState({ accessToken: res.data.access_token });
          window.localStorage.setItem("refreshToken", res.data.refresh_token);
          return true;
        })
        .catch((err) => {
          return false;
        });
    }
    return false;
  }

  getCarriers = () => {
    axios
      .get(`${process.env.REACT_APP_API_SERVICE_URL}/carriers`, {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.state.accessToken}`,
        },
      })
      .then((res) => {
        this.setState({ carriers: res.data });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  handleLoginFormSubmit = (data) => {
    const url = `${process.env.REACT_APP_API_SERVICE_URL}/auth/login`;
    axios
      .post(url, data)
      .then((res) => {
        this.getCarriers();
        this.setState({ accessToken: res.data.access_token });
        window.localStorage.setItem("refreshToken", res.data.refresh_token);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  onHandleLogoutUser = () => {
    window.localStorage.removeItem("refreshToken");
    this.setState({ accessToken: null });
  };

  render() {
    return (
      <div>
        <NavBar
          title={this.state.title}
          handleLogoutUser={this.onHandleLogoutUser}
          isAuthenticated={this.isAuthenticated}
        />
        <section className="section">
          <div className="container">
            <div className="columns">
              <div className="column is-half">
                <br />
                <Routes>
                  <Route
                    exact
                    path="/"
                    element={
                      <div>
                        <h1 className="title is-1">Test Genlogs</h1>
                        <hr />
                        <br />
                      </div>
                    }
                  />
                  <Route
                    exact
                    path="/login"
                    element={
                      <LoginForm
                        onLoginFormSubmit={this.handleLoginFormSubmit}
                        isAuthenticated={this.isAuthenticated}
                      />
                    }
                  />
                  <Route
                    exact
                    path="/status"
                    element={
                      <UserStatus
                        accessToken={this.state.accessToken}
                        isAuthenticated={this.isAuthenticated}
                      />
                    }
                  />
                  <Route
                    exact
                    path="/carriers"
                    element={
                      <CarriersList
                        carriers={this.state.carriers}
                        isAuthenticated={this.isAuthenticated}
                      />
                    }
                  />
                </Routes>
              </div>
            </div>
          </div>
        </section>
      </div>
    );
  }
}

export default App;
