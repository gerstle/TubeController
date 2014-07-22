var config = {
  programs: [
    "melt",
    "sparkle",
    "sparklemelt",
    "test",
    "fadeOut",
    "red"
  ],
  schedules: [
    {
      name: "main",
      shows: [
        {
          program: 'melt',
          length: 10
        },
        {
          program: 'sparkle',
          length: 20
        }
      ]
    },
    {
      name: "blah",
      shows: [
        {
          program: 'melt',
          length: 10
        },
        {
          program: 'test',
          length: 20
        }
      ]
    }
  ]
}
