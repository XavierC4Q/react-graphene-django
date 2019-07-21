import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter} from 'react-router-dom';
import {ApolloClient} from 'apollo-client';
import {InMemoryCache} from 'apollo-cache-inmemory';
import {ApolloProvider} from 'react-apollo';
import {createHttpLink} from 'apollo-link-http';
import {setContext} from 'apollo-link-context';
import {withClientState} from 'apollo-link-state';
import {ApolloLink} from 'apollo-link';
import gql from 'graphql-tag';
import App from './App';
import config from './config';

import * as serviceWorker from './serviceWorker';

const httpLink = createHttpLink({
  uri: config.GQL_HTTP
});

const authLink = setContext((operation) => {
  const authToken = localStorage.getItem('token');
  return {
    headers: {
      Authorization: authToken ? `JWT ${authToken}` : ''
    }
  };
});

const cache = new InMemoryCache();

const stateLink = withClientState({
  cache,
  resolvers: {
      Query: {
          getCurrentUser: (root: any, args: any, {cache}: {cache: any}) => {
              console.log('RESOLVING CURRENT');
              const data = cache.readQuery({
                  query: gql`
                    query getCurrentUser {
                        currentUser @client {
                            id
                            email
                            username
                            account
                        }
                    }
                  `
              });
              return data.currentUser;
          }
      }
  },
  defaults: {
    currentUser: null
  }
});

const client = new ApolloClient({
  link: ApolloLink.from([stateLink, authLink, httpLink]),
  cache
});

ReactDOM.render(
  <ApolloProvider client={client}>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </ApolloProvider>,
  document.getElementById('root')
);

serviceWorker.unregister();
