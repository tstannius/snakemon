import React from 'react';

import Button from 'react-bootstrap/Button'
import OverlayTriger from 'react-bootstrap/OverlayTrigger'
import Popover from 'react-bootstrap/Popover'

import { ReactComponent as ThreeDots } from '../assets/three-dots.svg';
import { ReactComponent as Trash } from '../assets/trash3.svg';

import { IComment } from "../interfaces"

import { useAuth } from "../hooks"
import { apiUrl } from '../env';

interface ICommentProps extends IComment {
    callbackUpdateOnDelete: () => void
}

export default function Comment(props: ICommentProps): JSX.Element {
    let auth = useAuth()

    // TODO: edit, delete ...
    function deleteComment(): void {
        const url = `${apiUrl}/workflows/comments?comment_id=${props.id}`
        const request = new Request(url, {
            method: 'DELETE',
            credentials: 'include', // necessary for cookies
            mode: "cors",
            headers: { 'Content-Type': 'application/json' },
          });
          fetch(request)
            .then((response) => {
                if (response.status === 200) {
                    // refresh comment list in parent
                    props.callbackUpdateOnDelete();
                } else if ((response.status >= 400) && (response.status <= 500)) {
                    response.json()
                        .then(data => {
                            console.log(data)
                        })
                }
            })
    }

    
    return(
        <div id="Comment-Container" className="p-2 border-top">
            <div id="CommentMetaData" className="d-flex">
                <div id="CommentMetadata-Title" className="me-auto p-1">
                    <span className="pe-2 align-middle fw-bold">{props.username}</span>
                    <span className="pe-2 align-middle">-</span> 
                    <span className="align-middle">{props.created_at}</span>
                </div>
                <div id="ComentMetadata-Actions" className="p-1">
                    {/* only show actions if logged in */}
                    {auth.user &&
                        <OverlayTriger
                            trigger="click"
                            placement="bottom"
                            rootClose
                            overlay={
                            <Popover id="popover-positioned-bottom"
                                className="shadow p-3 bg-body rounded"
                                style={{"width": "200px"}}>
                                <div id="ComentMetadata-ActionList">
                                    {/* only show delete for own posts */}
                                    {auth.user === props.username &&
                                    <button className="btn btn-light"
                                    type="button"
                                    style={{"width": "100%"}}
                                    onClick={() => deleteComment()}>
                                                <Trash className="me-2"/>
                                                <span className="align-middle">Delete</span>
                                    </button>
                                    }
                                </div>
                            </Popover>}>
                                <Button className="btn-sm btn-light"><ThreeDots /></Button>
                        </OverlayTriger>
                    }
                </div>
                
            </div>
            <div id="Comment-Content">
                {props.content}
            </div>
      </div>
    )
}
