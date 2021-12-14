import './BooleanField.css'

function BooleanField({field, ...props}) {
    return (
        <div className={'boolean-field' + (field.value ? ' checked' : '')} onClick={() => props.onClick(field)}>
            {field.name}
        </div>
    )
}

export default BooleanField