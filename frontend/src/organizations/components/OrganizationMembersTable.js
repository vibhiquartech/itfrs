/*
 * Presentational component
 */
import React from 'react';
import PropTypes from 'prop-types';
import ReactTable from 'react-table';
import FontAwesomeIcon from '@fortawesome/react-fontawesome';
import { Link } from 'react-router-dom';
import 'react-table/react-table.css';

import USERS from '../../constants/routes/Users';
import roleName from '../../utils/translate';

const OrganizationMembersTable = (props) => {
  const columns = [{
    accessor: item => `${item.firstName} ${item.lastName}`,
    className: 'col-name',
    Header: 'Name',
    id: 'name',
    minWidth: 150
  }, {
    accessor: item => item.roles &&
      item.roles.map(role => roleName(role)).join(', '),
    className: 'col-role',
    Header: 'Role(s)',
    id: 'role',
    minWidth: 200
  }, {
    accessor: item => item.email,
    className: 'col-status-display',
    Header: 'Email',
    id: 'email',
    minWidth: 200
  }, {
    accessor: item => item.phone,
    className: 'col-phone',
    Header: 'Phone',
    id: 'phone',
    minWidth: 100
  }, {
    accessor: item => (item.isActive ? 'Active' : 'Inactive'),
    className: 'col-status',
    Header: 'Status',
    id: 'status',
    minWidth: 100
  }, {
    accessor: item => item.id,
    Cell: (row) => {
      const viewUrl = USERS.DETAILS.replace(':id', row.value);

      return <Link to={viewUrl}><FontAwesomeIcon icon="eye" /></Link>;
    },
    className: 'col-actions',
    filterable: false,
    Header: '',
    id: 'actions',
    minWidth: 100
  }];

  const filterMethod = (filter, row, column) => {
    const id = filter.pivotId || filter.id;
    return row[id] !== undefined ? String(row[id])
      .toLowerCase()
      .includes(filter.value.toLowerCase()) : true;
  };

  const filterable = true;

  return (
    <ReactTable
      data={props.items}
      defaultPageSize={15}
      defaultSorted={[{
        id: 'name',
        desc: false
      }]}
      filterable={filterable}
      pageSizeOptions={[5, 10, 15, 20, 25, 50, 100]}
      defaultFilterMethod={filterMethod}
      columns={columns}
    />
  );
};

OrganizationMembersTable.propTypes = {
  items: PropTypes.arrayOf(PropTypes.shape({
    email: PropTypes.string,
    firstName: PropTypes.string,
    id: PropTypes.number,
    isActive: PropTypes.bool,
    lastName: PropTypes.string,
    role: PropTypes.shape({
      id: PropTypes.number
    })
  })).isRequired
};

export default OrganizationMembersTable;
