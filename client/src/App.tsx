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

interface IData {
  users: {
    users: IUser[];
  };
}

const App = () => {
  return (
    <div>
      <Query<IData> query={QUERY}>
        {({loading, data, error}) => {
          if (loading) return <div>Loading stuff...</div>;
          if (error) return <div>Errors</div>;
          console.log(data);
          return <Login />;
        }}
      </Query>
    </div>
  );
};

export default App;
