import React, { Component } from "react";
import PropTypes from "prop-types";
import axios from "axios";
import { Navigate } from "react-router-dom";

class UserStatus extends Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      username: "",
    };
  }
  componentDidMount() {
    this.getUserStatus();
  }
  getUserStatus(event) {
    const options = {
      url: `${process.env.REACT_APP_API_SERVICE_URL}/auth/status`,
      method: "get",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.props.accessToken}`,
      },
    };
    return axios(options)
      .then((res) => {
        this.setState({ email: res.data.email, username: res.data.username });
        console.log("data:" + res.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }
  render() {
    if (!this.props.isAuthenticated()) {
      return <Navigate to="/login" replace />;
    }
    return (
      <div>
        <h1 className="title is-4">Welcome user:</h1>&nbsp;
        <p className="box title is-6 username">{this.state.username}</p>
      </div>
    );
  }
}

UserStatus.propTypes = {
  accessToken: PropTypes.string,
  isAuthenticated: PropTypes.func.isRequired,
};

export default UserStatus;
