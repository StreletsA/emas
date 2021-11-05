import logo from './logo.svg';
import MainTable from './base/MainTable';

export const host = 'http://127.0.0.1:5000/emas/api/';

function App() {
  return (
    <div className='root'>
      <MainTable />
    </div>
  )
}

export default App;
