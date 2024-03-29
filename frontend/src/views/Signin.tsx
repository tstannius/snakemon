import React, { useState } from 'react';
import { useNavigate } from 'react-router';

import 'bootstrap/dist/css/bootstrap.min.css';
import Alert from 'react-bootstrap/Alert'
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form';

import { Logo } from "../components";
import { useAuth } from "../hooks"



export default function Signin(): JSX.Element {
    const [username, setUsername] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [validated, setValidated] = useState<boolean>(false);
    const [warning, setWarning] = useState<string>("");
    let navigate = useNavigate();
    let auth = useAuth();

    function handleSubmit(event: React.SyntheticEvent) {
        // manually prevent reload page on submit, as
        // this will clear the warning if login creds invalid
        event.preventDefault();
        const form = (event.currentTarget as HTMLFormElement);
        // TODO: use submission as done in react router tutorial:
        // https://stackblitz.com/github/remix-run/react-router/tree/main/examples/auth?file=src/App.tsx
        if (form.checkValidity() === false) {
            event.stopPropagation();
        } else {
            // signin with callbackSuccess and callbackError
            auth.signin(
                username, 
                password, 
                () => {navigate("/")}, 
                (msg: string) => {
                    setWarning(msg);
                    setPassword("");
            })
        }
        setValidated(true);
    }

    return (
        <div id="SigninContainer" 
            className="position-relative m-auto" 
            style={{paddingTop: "40px", width: "350px"}}>
                <div id="SigninLogo" className="d-flex justify-content-center my-5 fs-1">
                    <Logo />
                </div>
                <div id="SigninForm">
                    {
                    // show warning if set
                    warning.length > 0 &&
                        <Alert className="py-2" variant="danger">{warning}</Alert>
                    }

                    <Form noValidate validated={validated} onSubmit={handleSubmit}>
                    <Form.Group className="mb-3" controlId="formUsername">
                        <Form.Label>Username</Form.Label>
                        <Form.Control 
                            required
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setUsername(e.currentTarget.value)}
                            />
                        <Form.Control.Feedback type="invalid">
                            Please enter username.
                        </Form.Control.Feedback>
                    </Form.Group>

                    <Form.Group className="mb-3" controlId="formPassword">
                        <Form.Label>Password</Form.Label>
                        <Form.Control type="password" placeholder="Password"
                            required
                            value={password}
                            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
                            setPassword(e.currentTarget.value)}
                            />
                        <Form.Control.Feedback type="invalid">
                            Please enter password.
                        </Form.Control.Feedback>
                    </Form.Group>
                    <Button variant="primary" style={{"width": "100%", "backgroundColor": "var(--sm-green-bright", "borderColor": "var(--sm-green-bright"}}
                        type="submit">
                        Submit
                    </Button>
                    </Form>
                </div>
        </div>
    )
};
