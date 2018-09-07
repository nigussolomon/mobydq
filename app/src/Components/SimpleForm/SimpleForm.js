import React from 'react';
import { withFormik } from 'formik';
import TextInput from './../FormInput/TextInput';
import SelectInput from './../FormInput/SelectInput';
import SimpleButton from './../FormInput/SimpleButton';

class SimpleForm extends React.Component {
  render() {
    return(
      <React.Fragment>
        <MyEnhancedForm
          data={this.props.data}
          indicator={{ name: '', description: '', executionOrder: 0, indicatorType: "", indicatorGroup: ""}}
        />
      </React.Fragment>
    )
  }
}


const MyForm = props => {
  const {
    data,
    values,
    touched,
    errors,
    dirty,
    handleChange,
    handleBlur,
    handleSubmit,
    handleReset,
    isSubmitting,
  } = props;
  return (
    <form onSubmit={handleSubmit}>
      <TextInput
        id="name"
        label="Indicator name"
        helperText=""
        placeholder="Enter indicator name"
        touched={touched.name}
        errors={errors.name}
        error={touched.name && errors.name}
        value={values.name}
        onChange={handleChange}
        onBlur={handleBlur}
      />
       <TextInput
        id="description"
        label="Indicator Description"
        helperText=""
        placeholder="Enter decription name"
        touched={touched.description}
        errors={errors.description}
        error={touched.description && errors.description}
        value={values.description}
        onChange={handleChange}
        onBlur={handleBlur}
      />
      <TextInput
          id="executionOrder"
          label="Execution Order"
          helperText=""
          numeric={true}
          touched={touched.executionOrder}
          errors={errors.executionOrder}
          error={touched.executionOrder && errors.executionOrder}
          value={values.executionOrder}
          onChange={handleChange}
          onBlur={handleBlur}
      />
      <SelectInput
        id="indicatorType"
        label="Indicator Type"
        items={data.allIndicatorTypes.nodes}
        touched={touched.indicatorType}
        errors={errors.indicatorType}
        error={touched.indicatorType && errors.indicatorType}
        value={values.indicatorType}
        onChange={handleChange}
        onBlur={handleBlur}
      />
      <SelectInput
        id="indicatorGroup"
        label="Indicator Group"
        items={data.allIndicatorGroups.nodes}
        touched={touched.indicatorGroup}
        errors={errors.indicatorGroup}
        error={touched.indicatorGroup && errors.indicatorGroup}
        value={values.indicatorGroup}
        onChange={handleChange}
        onBlur={handleBlur}
      />
      <SimpleButton
        type="reset"
        label="Reset"
        onClick={handleReset}
        disabled={!dirty || isSubmitting}
      />
      <SimpleButton
          type="submit"
          disabled={isSubmitting}
          label="Submit"
      />
      <DisplayFormikState {...props} />
    </form>
  );
};

const formikEnhancer = withFormik({
  // validationSchema: Yup.object().shape({
  //   firstName: Yup.string()
  //     .min(2, "C'mon, your name is longer than that")
  //     .required('First name is required.'),
  //   lastName: Yup.string()
  //     .min(2, "C'mon, your name is longer than that")
  //     .required('Last name is required.'),
  //   email: Yup.string()
  //     .email('Invalid email address')
  //     .required('Email is required!'),
  // }),

  mapPropsToValues: ({ indicator }) => ({
    ...indicator,
  }),
  handleSubmit: (payload, { setSubmitting }) => {
    alert(payload.name);
    setSubmitting(false);
  },
  displayName: 'MyForm',
});

const DisplayFormikState = props =>
  <div style={{ margin: '1rem 0' }}>
    <h3 style={{ fontFamily: 'monospace' }} />
    <pre
      style={{
        background: '#f6f8fa',
        fontSize: '.65rem',
        padding: '.5rem',
      }}
    >
      <strong>props</strong> ={' '}
      {JSON.stringify(props, null, 2)}
    </pre>
  </div>;


const MyEnhancedForm = formikEnhancer(MyForm);

export default SimpleForm;