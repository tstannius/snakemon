import React from 'react';
import { Link } from "react-router-dom";
import { ReactComponent as Favicon } from '../assets/favicon.svg';



export default function Logo(): JSX.Element {
    return(
      // no link underline, font size 100% of parent,
      <div>
        <Link className="text-decoration-none" 
          style={{
            color: "black",
            fontSize: "100%"
          }}
          to="/">
          <Favicon style={{}}/>{' '}
          <span>SnakeMon</span>
        </Link>
      </div>
    )
}
