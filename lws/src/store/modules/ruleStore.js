const ruleStore = {
    namespace: true,
    state: {
        rules: {
            required: value => !!value || 'Required',
            minvalue: value => value.length >= 8 || 'At least 8 characters',
            email: value => {
                const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                return pattern.test(value) || 'Invalid e-mail.'
            },
            samevalues: (value1, value2) => {
                return value1 === value2 || 'Must be equal'
            }
        }
    }
}

export default ruleStore