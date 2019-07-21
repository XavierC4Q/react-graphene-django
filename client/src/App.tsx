import * as React from 'react';
import gql from 'graphql-tag';
import {Query} from 'react-apollo';
import {IUser} from './types/user';

import Login from './components/auth/Login';

const QUERY = gql`
  query users {
    users {
      id
      username
    }
  }
`;

const GET_CURRENT_USER = gql`
  query getCurrentUser {
    getCurrentUser @client
  }
`;

interface IData {
  users: {
    users: IUser[];
  };
}

interface ITestCurrentData {
  currentUser: null | IUser;
}

const TestCurrent = () => {
  return (
    <Query<ITestCurrentData> query={GET_CURRENT_USER}>
      {({loading, error, data}) => {
        if (loading) return <div>Loading current user...</div>;
        if (error) return <div>Err on current</div>;
        return <div>Got em</div>;
      }}
    </Query>
  );
};

const App = () => {
  return (
    <div>
      <Query<IData> query={QUERY}>
        {({loading, data, error}) => {
          if (loading) return <div>Loading stuff...</div>;
          if (error) return <div>Errors</div>;
          return (
            <React.Fragment>
              <Login />
              <TestCurrent />
            </React.Fragment>
          );
        }}
      </Query>
    </div>
  );
};

export default App;
