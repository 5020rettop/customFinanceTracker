{/*
###########################################################################
#     Narcissist - The 1975
#   Written by Chutipon (Potter) Chutipanich 
#           2025-12-12
########################################################################### */};

{/*
###########################################################################
#
#   region Imports
#
########################################################################### */}
import { useState, useEffect } from 'react';
import api from '../api/axios';
import { useNavigate } from 'react-router-dom';

{/*
###########################################################################
#
#   region Helpers
#
########################################################################### */}

{/*
###########################################################################
#
#   region Program Specific Globals
#
########################################################################### */}

{/*
###########################################################################
#
#   region Class Definitions
#
########################################################################### */}

const Dashboard = () => {
  const [ transactions, setTransactions ] = useState([]);
  const [ categories, setCategories ] = useState([]);
  // form state
  const [ amount, setAmount] = useState('');
  const [ description, setDescription] = useState('');
  const [ date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [ time, setTime] = useState(new Date().toTimeString().substring(0, 8));
  const [ type, setType] = useState('expense');
  const [ categoryId, setCategoryId] = useState('');
  
  const navigate = useNavigate();

  // fetch data on component mount
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [ transRes, catRes ] = await Promise.all([
          api.get( '/transactions/' ),
          api.get( '/categories/' )
        ] );
        setTransactions( transRes.data );
        setCategories( catRes.data );
        // checks for categories existing and set first one as default
        if ( catRes.data.length > 0 ) setCategoryId( catRes.data[0].id );
      } catch ( err ) {
        console.error( "Error fetching data", err );
        // if unauthorized, redirect to login
        if ( err.response && err.response.status === 401 ) { // 401 Unauthorized
            navigate('/login');
        }
      }
    };
    fetchData();
  }, [ navigate ]);

  // handle add transaction
  const handleAddTransaction = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post( '/transactions/', {
        amount: parseFloat( amount ),
        description,
        date,
        time,
        type,
        category_id: parseInt( categoryId )
      } );
      // add new transaction to the list immediately
      setTransactions( [ ...transactions, response.data ] );
      // reset description/amount for convenience
      setAmount('');
      setDescription('');
    } catch ( err ) {
      console.error( "Failed to add transaction", err );
      alert( "Error adding transaction" );
    }
  };

  // handle delete
  const handleDelete = async (id) => {
    if ( !confirm( "Are you sure?" ) ) return;
    try {
        await api.delete( `/transactions/${id}` );
        setTransactions( transactions.filter( t => t.id !== id ) );
    } catch (err) {
        console.error( "Failed to delete", err );
    }
  };
  // handle logout
  const handleLogout = () => {
    localStorage.removeItem( 'token' );
    navigate( '/login' );
  };

  return (
    <div style={{ maxWidth: '1600px', margin: '2rem auto', padding: '0 1rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>My Finance Dashboard</h2>
        <button onClick={handleLogout} style={{ background: '#ff4444', color: 'white', border: 'none', padding: '8px 16px', cursor: 'pointer' }}>
          Logout
        </button>
      </div>

      {/* --- Add Transaction Form --- */}
      <div style={{ background: '#404040ff', padding: '1.5rem', borderRadius: '8px', marginTop: '1rem' }}>
        <h3>Add New Transaction</h3>
        <form onSubmit={handleAddTransaction} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            
            <input 
                type="number" step="0.01" placeholder="Amount" required 
                value={amount} onChange={(e) => setAmount(e.target.value)}
                style={{ padding: '8px' }} 
            />
            
            <input 
                type="text" placeholder="Description" required 
                value={description} onChange={(e) => setDescription(e.target.value)}
                style={{ padding: '8px' }} 
            />

            <input 
                type="date" required 
                value={date} onChange={(e) => setDate(e.target.value)}
                style={{ padding: '8px' }} 
            />

             <input 
                type="time" required 
                value={time} onChange={(e) => setTime(e.target.value)}
                style={{ padding: '8px' }} 
            />

            <select value={type} onChange={(e) => setType(e.target.value)} style={{ padding: '8px' }}>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
            </select>

            <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)} style={{ padding: '8px' }}>
                {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                ))}
            </select>

            <button type="submit" style={{ padding: '8px', background: '#4CAF50', color: 'white', border: 'none', cursor: 'pointer' }}>
                Add Transaction
            </button>
        </form>
      </div>

      {/* --- Transactions List --- */}
      <h3 style={{ marginTop: '2rem' }}>Recent Transactions</h3>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '1rem' }}>
        <thead>
            <tr style={{ textAlign: 'left', borderBottom: '2px solid #ddd' }}>
                <th style={{ padding: '10px' }}>Date</th>
                <th style={{ padding: '10px' }}>Time</th>
                <th style={{ padding: '10px' }}>Description</th>
                <th style={{ padding: '10px' }}>Category</th>
                <th style={{ padding: '10px' }}>Type</th>
                <th style={{ padding: '10px' }}>Amount</th>
                <th style={{ padding: '10px' }}>Action</th>
            </tr>
        </thead>
        <tbody>
          { [...transactions]
            .sort( (b, a) => a.time.localeCompare(b.time) ) // sort by time ascending
            .sort( (b, a) => new Date(a.date) - new Date(b.date) ) // sort by date ascending
            .map(t => (
                <tr key={t.id} style={{ borderBottom: '1px solid #eee' }}>
                    <td style={{ padding: '10px' }}>{t.date}</td>
                    <td style={{ padding: '10px' }}>{t.time}</td>
                    <td style={{ padding: '10px' }}>{t.description}</td>
                    <td style={{ padding: '10px' }}>{t.category ? t.category.name : '-'}</td>
                    <td style={{ padding: '10px', color: t.type === 'income' ? 'green' : 'red' }}>
                        {t.type}
                    </td>
                    <td style={{ padding: '10px', fontWeight: 'bold' }}>
                        ${t.amount.toFixed(2)}
                    </td>
                    <td style={{ padding: '10px' }}>
                        <button onClick={() => handleDelete(t.id)} style={{ color: 'red', border: 'none', background: 'none', cursor: 'pointer' }}>
                            X
                        </button>
                    </td>
                </tr>
            ))}
        </tbody>
      </table>
    </div>
  );
};

export default Dashboard;