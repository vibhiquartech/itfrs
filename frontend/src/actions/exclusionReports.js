import axios from 'axios';
import { call, put, select, takeLatest, delay } from 'redux-saga/effects';

import * as Routes from '../constants/routes';
import { GenericRestTemplate } from './base/genericTemplate';

class ExclusionReportRestInterface extends GenericRestTemplate {
  constructor (name, baseUrl, stateName) {
    super(name, baseUrl, stateName);

    this.validateHandler = this.validateHandler.bind(this);
    this.doValidate = this.doValidate.bind(this);
  }

  // eslint-disable-next-line class-methods-use-this
  getCustomIdentityActions () {
    return ['VALIDATE', 'VALIDATE_SUCCESS'];
  }

  // eslint-disable-next-line class-methods-use-this
  getCustomDefaultState () {
    return {
      isValidating: false,
      validationMessages: {},
      validationPassed: null,
      isRecomputing: false,
      recomputeResult: {}
    };
  }

  getCustomReducerMap () {
    return [
      [this.validate, (state, action) => ({
        ...state,
        isValidating: true,
        validationState: action.payload || null,
        validationMessages: {},
        validationPassed: null
      })],
      [this.validateSuccess, (state, action) => ({
        ...state,
        isValidating: false,
        validationState: null,
        validationMessages: action.payload,
        validationPassed: Object.keys(action.payload).length === 0
      })]
    ];
  }

  validationStateSelector () {
    const sn = this.stateName;

    return state => (state.rootReducer[sn].validationState);
  }

  doValidate (data = null) {
    const { id, state } = data;
    return axios.post(`${this.baseUrl}/${id}/validate_partial`, state);
  }

  * validateHandler () {
    yield delay(1000); // debounce

    const data = yield (select(this.validationStateSelector()));

    try {
      const response = yield call(this.doValidate, data);
      yield put(this.validateSuccess(response.data));
    } catch (error) {
      yield put(this.error(error.response.data));
    }
  }

  getCustomSagas () {
    return [
      takeLatest(this.validate, this.validateHandler)
    ];
  }
}

const exclusionReports = new ExclusionReportRestInterface(
  'EXCLUSION_REPORT',
  Routes.BASE_URL + Routes.COMPLIANCE_REPORTING_API,
  'exclusionReports'
);

// eslint-disable-next-line import/prefer-default-export
export { exclusionReports };
