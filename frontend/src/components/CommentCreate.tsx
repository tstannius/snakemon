import React, { useState } from 'react';
import { useParams } from "react-router-dom";

import Button from 'react-bootstrap/Button'
import InputGroup from "react-bootstrap/InputGroup"
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';

import { apiUrl } from '../env';
import { IComment } from "../interfaces"

interface ICommentCreateProps {
    callbackUpdate: (comment: IComment) => void
}

export default function CommentCreate(props: ICommentCreateProps): JSX.Element {
    let [comment, setComment] = useState<string>("");
    let { workflowId } = useParams();

    function postComment() {
        const ur = `${apiUrl}/workflows/${workflowId}/comments`
        const request = new Request(ur, {
            method: 'POST',
            credentials: 'include', // necessary for cookies
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ content: comment })
          });
          fetch(request)
            .then((response) => {
                // TODO: handle other responses?
                if (response.status === 201) {
                    response.json()
                        .then(data => {
                            setComment("");
                            props.callbackUpdate(data);
                        })
                } else if ((response.status >= 400) && (response.status <= 500)) {
                    response.json()
                        .then(data => {
                            console.log(data)
                        })
                }
            })
    }

    function handleSubmit(event: React.SyntheticEvent) {
        // manually prevent reload page on submit, as
        // this will clear the warning if login creds invalid
        event.preventDefault();
        const form = (event.currentTarget as HTMLFormElement);
        
        if (form.checkValidity() === false) {
            event.stopPropagation();
        } else {
            postComment();
        }
    }

    return(
        <div id="CommentCreate-Container" className="p-2 border-top">
            <div id="CommentCreate-Form">
                <div id="CommentCreate-Fields">
                <Form onSubmit={handleSubmit}>
                    <InputGroup className="mb-3">
                        <FormControl 
                                required
                                as="textarea"
                                aria-label="With textarea"
                                placeholder="Write a comment"
                                value={comment}
                                onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
                                    setComment(e.currentTarget.value)}
                                }
                                />
                    </InputGroup>
                    <Button 
                        variant="primary" 
                        disabled={(comment.length === 0)}
                        style={{"width": "100%", 
                                // "backgroundColor": "var(--sm-green-bright", 
                                // "borderColor": "var(--sm-green-bright"
                                }
                            }
                        type="submit">
                        Post
                    </Button>
                </Form>
                </div>
            </div>
        </div>
    )
}
