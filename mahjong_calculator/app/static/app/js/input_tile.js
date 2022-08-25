const app = new Vue({
  el: "#input_tile",
  data() {
    return {
      tiles: [
        { id: "1m", url: "../../static/app/images/hai_1m.jpg" },
        { id: "2m", url: "../../static/app/images/hai_2m.jpg" },
        { id: "3m", url: "../../static/app/images/hai_3m.jpg" },
        { id: "4m", url: "../../static/app/images/hai_4m.jpg" },
        { id: "5m", url: "../../static/app/images/hai_5m.jpg" },
        { id: "6m", url: "../../static/app/images/hai_6m.jpg" },
        { id: "7m", url: "../../static/app/images/hai_7m.jpg" },
        { id: "8m", url: "../../static/app/images/hai_8m.jpg" },
        { id: "9m", url: "../../static/app/images/hai_9m.jpg" },
        { id: "1s", url: "../../static/app/images/hai_1s.jpg" },
        { id: "2s", url: "../../static/app/images/hai_2s.jpg" },
        { id: "3s", url: "../../static/app/images/hai_3s.jpg" },
        { id: "4s", url: "../../static/app/images/hai_4s.jpg" },
        { id: "5s", url: "../../static/app/images/hai_5s.jpg" },
        { id: "6s", url: "../../static/app/images/hai_6s.jpg" },
        { id: "7s", url: "../../static/app/images/hai_7s.jpg" },
        { id: "8s", url: "../../static/app/images/hai_8s.jpg" },
        { id: "9s", url: "../../static/app/images/hai_9s.jpg" },
        { id: "1p", url: "../../static/app/images/hai_1p.jpg" },
        { id: "2p", url: "../../static/app/images/hai_2p.jpg" },
        { id: "3p", url: "../../static/app/images/hai_3p.jpg" },
        { id: "4p", url: "../../static/app/images/hai_4p.jpg" },
        { id: "5p", url: "../../static/app/images/hai_5p.jpg" },
        { id: "6p", url: "../../static/app/images/hai_6p.jpg" },
        { id: "7p", url: "../../static/app/images/hai_7p.jpg" },
        { id: "8p", url: "../../static/app/images/hai_8p.jpg" },
        { id: "9p", url: "../../static/app/images/hai_9p.jpg" },
        { id: "1h", url: "../../static/app/images/hai_1h.jpg" },
        { id: "2h", url: "../../static/app/images/hai_2h.jpg" },
        { id: "3h", url: "../../static/app/images/hai_3h.jpg" },
        { id: "4h", url: "../../static/app/images/hai_4h.jpg" },
        { id: "5h", url: "../../static/app/images/hai_5h.jpg" },
        { id: "6h", url: "../../static/app/images/hai_6h.jpg" },
        { id: "7h", url: "../../static/app/images/hai_7h.jpg" },
      ],
      closedTiles: [],
      meltedTiles: [],
      winTile: [],
      doraTiles: [],
    };
  },
  methods: {
    addClosed(id) {
      const selected = this.tiles.find((tile) => {
        return id === tile.id;
      });
      this.closedTiles.push(selected);
    },
    addMelted(id) {
      const selected = this.tiles.find((tile) => {
        return id === tile.id;
      });
      this.meltedTiles.push(selected);
    },
    addWin(id) {
      const selected = this.tiles.find((tile) => {
        return id === tile.id;
      });
      this.winTile.push(selected);
    },
    addDora(id) {
      const selected = this.tiles.find((tile) => {
        return id === tile.id;
      });
      this.doraTiles.push(selected);
    },
    deleteClosed(index) {
      this.closedTiles.splice(index, 1);
    },
    deleteMelted(index) {
      this.meltedTiles.splice(index, 1);
    },
    deleteWin(index) {
      this.winTile.splice(index, 1);
    },
    deleteDora(index) {
      this.doraTiles.splice(index, 1);
    },
    query() {
      const queryClosed = this.closedTiles.reduce((prev, item) => {
        return prev + item.id + ",";
      }, "");
      const queryMelted = this.meltedTiles.reduce((prev, item) => {
        return prev + item.id + ",";
      }, "");
      const queryWin = this.WinTile;
      const queryDora = this.doraTiles.reduce((prev, item) => {
        return prev + item.id + ",";
      }, "");
      console.log(
        JSON.stringify({
          closed: queryClosed,
          melted: queryMelted,
          win: queryWin,
          dora: queryDora,
        })
      );
      return JSON.stringify({
        closed: queryClosed,
        melted: queryMelted,
        win: queryWin,
        dora: queryDora,
      });
    },
  },
  computed: {},
});
