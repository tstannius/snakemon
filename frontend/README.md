# TODO
### Need
- Improve table view
  - Sort data (default: started_at, recent-to-old)
  - Pagination (limit to 30?)
  - Get latest data, i.e. rows last inserted
  - Handle react-tables types: https://github.com/DefinitelyTyped/DefinitelyTyped/tree/master/types/react-table#configuration-using-declaration-merging
- Cleanup and organize components

### Done
- Choose component framework, see. https://www.npmtrends.com/antd-vs-material-ui-vs-react-bootstrap-vs-reactstrap-vs-rsuite
   1. Best choice seems to be plain css for as much as possible with react-bootstrap for some things
   2. A component framework specifically for tables can be used, if necessary
- Add navbar and routing
   1. Base on react-router tutorial: https://stackblitz.com/github/remix-run/react-router/tree/main/examples/basic?file=src%2FApp.tsx
   2. Alternatives: base CSS and bootstrap https://stackoverflow.com/questions/50166035/how-to-implement-navbar-using-react
   3. Other example: https://www.geeksforgeeks.org/create-a-responsive-navbar-using-reactjs/
- Add workflows view
   1. Try react-bootstrap first
   2. Example for how to get just some data and not all
   3. Fancy table library, see https://react-table.tanstack.com/# Getting Started with Create React App

### Nice (Later)
##### More robust API calls with TS typing
```
// for more robust TS api calls
// https://www.sohamkamani.com/typescript/rest-http-api-call/
// https://www.freecodecamp.org/news/make-typescript-easy-using-basic-ts-generics/
// interface Workflow {
//   workflow: string
//   name: string
//   id: number
//   status: string
//   done: number
//   total: number
//   started_at: string
//   completed_at: string
//   last_update_at: string
// }
```

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can’t go back!**

If you aren’t satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you’re on your own.

You don’t have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn’t feel obligated to use this feature. However we understand that this tool wouldn’t be useful if you couldn’t customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).
