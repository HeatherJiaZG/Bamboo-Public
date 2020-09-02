#pragma once

class table_t;
class Catalog;
class txn_man;
struct TsReqEntry;
class Row_ic3;

#define LOCK_BIT (1UL << 63)
#if CC_ALG == IC3

struct IC3LockEntry {
  access_t             type;
  txn_man *            txn;
  uint64_t             txn_id;
  IC3LockEntry *          prev;
  IC3LockEntry *          next;
};

class Cell_ic3 {
 public:
  void                  init(row_t * orig_row, int id);
  /* copy to corresponding col of local row */
  void                  access(row_t * local_row, Access *txn_access);
  bool                  try_lock();
  uint64_t              get_tid() {return _tid_word;};
  void                  add_to_acclist(txn_man * txn, access_t type);
  void                  rm_from_acclist(txn_man * txn);
  IC3LockEntry *           get_last_writer();
  IC3LockEntry *           get_last_accessor();
  void                  release();
 private:
  row_t * 			    _row;
  Row_ic3 *             row_manager;
  volatile uint64_t	    _tid_word;
  int                   idx;
  IC3LockEntry *           acclist;
  IC3LockEntry *           acclist_tail;
};

class Row_ic3 {
 public:
  void 				init(row_t * row);
  RC 				access(txn_man * txn, row_t * local_row); // row-level
  void                access(row_t * local_row, int idx, Access * txn_access);// cell-level
  bool                try_lock(int idx);
  void 				assert_lock() {assert(_tid_word & LOCK_BIT);};
  uint64_t          get_tid(int idx) {return cell_managers[idx].get_tid();};
  void              add_to_acclist(int idx, txn_man * txn, access_t type) {
    cell_managers[idx].add_to_acclist(txn, type);
  };
  IC3LockEntry *       get_last_writer(int idx) {
    return cell_managers[idx].get_last_writer();};
  IC3LockEntry *       get_last_accessor(int idx) {
    return cell_managers[idx].get_last_accessor();};
  void              release(int idx) {return cell_managers[idx].release();};
  void              rm_from_acclist(int idx, txn_man * txn) {
    cell_managers[idx].rm_from_acclist(txn);
  };
 private:
  Cell_ic3 *        cell_managers;
  volatile uint64_t	_tid_word;
  row_t * 			_row;
};

#endif
