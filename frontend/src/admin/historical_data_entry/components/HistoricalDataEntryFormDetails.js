/*
 * Presentational component
 */
import React from 'react';
import PropTypes from 'prop-types';
import numeral from 'numeral';

import * as Lang from '../../../constants/langEnUs';
import * as NumberFormat from '../../../constants/numeralFormats';

import HistoricalDataEntryFormNote from './HistoricalDataEntryFormNote';

const HistoricalDataEntryFormDetails = props => (
  <div className="historical-data-entry-form-details">
    <div className="main-form">
      <div className="form-row">
        <div className="col-md-6">
          <div className="form-group">
            <label htmlFor="effective-date">Effective Date:
              <input
                type="date"
                className="form-control"
                id="effective-date"
                name="effectiveDate"
                value={props.fields.effectiveDate}
                placeholder="Effective Date"
                onChange={props.handleInputChange}
                required="required"
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="transfer-type">Transfer Type:
              <div className="btn-group" role="group">
                <button type="button" className="btn btn-default">Credit Transfer</button>
                <button type="button" className="btn btn-default">Part 3 Award</button>
                <button type="button" className="btn btn-default">Validation</button>
                <button type="button" className="btn btn-default">Reduction</button>
              </div>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="credits-from">Credits From:
              <select
                className="form-control"
                id="credits-from"
                name="creditsFrom"
                value={props.fields.creditsFrom.id}
                onChange={props.handleInputChange}
                required="required"
              >
                <option key="0" value="" default />
                {props.fuelSuppliers &&
                  props.fuelSuppliers.map(organization => (
                    <option key={organization.id} value={organization.id}>
                      {organization.name}
                    </option>
                  ))}
              </select>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="credits-to">Credits To:
              <select
                className="form-control"
                id="credits-to"
                name="creditsTo"
                value={props.fields.creditsTo.id}
                onChange={props.handleInputChange}
                required="required"
              >
                <option key="0" value="" default />
                {props.fuelSuppliers &&
                  props.fuelSuppliers.map(organization => (
                    <option key={organization.id} value={organization.id}>
                      {organization.name}
                    </option>
                  ))}
              </select>
            </label>
          </div>
        </div>
        <div className="col-md-6">
          <div className="form-group">
            <label htmlFor="number-of-credits">Number of Credits:
              <input
                type="number"
                className="form-control"
                id="number-of-credits"
                name="numberOfCredits"
                value={props.fields.numberOfCredits}
                onChange={props.handleInputChange}
                required="required"
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="dollar-per-credit">Dollar per Credit:
              <input
                type="number"
                data-number-to-fixed="2"
                className="form-control"
                id="dollar-per-credit"
                name="dollarPerCredit"
                value={props.fields.dollarPerCredit}
                placeholder="Amount"
                onChange={props.handleInputChange}
                required="required"
              />
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="dollar-per-credit">...for a total of:
              <div className="form-control dollar-per-credit">{numeral(props.totalValue).format(NumberFormat.CURRENCY)}</div>
            </label>
          </div>

          <div className="form-group">
            <label htmlFor="transfer-type">Zero Dollar Reason:
              <div className="btn-group" role="group">
                <button type="button" className="btn btn-default">Affiliate</button>
                <button type="button" className="btn btn-default">Other</button>
              </div>
            </label>
          </div>
        </div>
      </div>

      <div className="row">
        <div className="col-md-12">
          <HistoricalDataEntryFormNote
            note={props.fields.note}
            handleInputChange={props.handleInputChange}
          />
        </div>
      </div>

      <div className="row">
        <div className="col-md-12">
          <div className="form-group btn-container">
            <button
              type="button" 
              className="btn btn-primary"
            >
              {Lang.BTN_ADD_TO_QUEUE}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
);

HistoricalDataEntryFormDetails.propTypes = {
  fuelSuppliers: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  fields: PropTypes.shape({
    creditsFrom: PropTypes.shape({
      name: PropTypes.string,
      id: PropTypes.number
    }),
    creditsTo: PropTypes.shape({
      name: PropTypes.string,
      id: PropTypes.number
    }),
    effectiveDate: PropTypes.instanceOf(Date),
    numberOfCredits: PropTypes.string,
    dollarPerCredit: PropTypes.string,
    note: PropTypes.string.isRequired,
    transferType: PropTypes.shape({
      name: PropTypes.string,
      id: PropTypes.number
    }),
    zeroDollarReason: PropTypes.string
  }).isRequired,
  handleInputChange: PropTypes.func.isRequired,
  totalValue: PropTypes.number.isRequired
};

export default HistoricalDataEntryFormDetails;
