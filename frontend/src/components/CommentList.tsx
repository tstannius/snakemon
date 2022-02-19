import React, { useEffect, useState } from 'react';

import { apiUrl } from '../env';

import { Comment, CommentCreate } from "../components"
import { useAuth } from "../hooks"
import { IComment } from "../interfaces"

interface ICommentListProps {
    workflowId: any
}

export default function CommentList(props: ICommentListProps): JSX.Element {
    let [comments, setComments] = useState<Array<IComment>>([]);
    let auth = useAuth();

    function getComments(): void {
        const request = new Request(`${apiUrl}/workflows/${props.workflowId}/comments`, {
            method: 'GET',
            credentials: 'include', // necessary for cookies
          });
          fetch(request)
            .then((response) => {
                if (response.status === 200) {
                    response.json()
                        .then(data => {
                            setComments(data)
                        })
                } else if ((response.status >= 400) && (response.status <= 500)) {
                    response.json()
                        .then(data => {
                            console.log(data.detail)
                        })
                }
            })
    }

    function updateComments(comment: IComment): void {
        setComments([...comments, comment])
    }

    useEffect(() => {
        getComments();
      }, []) // The empty array ensures the useEffect is only run once

    return(
        <div id="CommentList">
            <div id="Comments-List">
                {comments.map((comment) => (
                    <Comment key={comment.id}
                            id={comment.id} 
                            workflow_id={comment.workflow_id}
                            username={comment.username} 
                            content={comment.content} 
                            created_at={comment.created_at}
                            callbackUpdateOnDelete={getComments}/>
                ))}
                {/* only show if logged in */}
                {auth.user && 
                    <CommentCreate callbackUpdate={updateComments}/>}
            </div>
        </div>
    )
}
