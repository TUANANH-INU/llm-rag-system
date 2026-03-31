import './SystemStatus.css'

function SystemStatus({ status }) {
  return (
    <div className="system-status">
      <div className={`status-indicator ${status}`}></div>
      <span className="status-text">
        {status === 'loading' && 'Loading...'}
        {status === 'ready' && 'System Ready'}
        {status === 'error' && 'System Error'}
      </span>
    </div>
  )
}

export default SystemStatus
