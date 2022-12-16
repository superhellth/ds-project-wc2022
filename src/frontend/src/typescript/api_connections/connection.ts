/**
 * Abstract connection class.
 */
abstract class Connection {

    protected readonly URL: string;

    public constructor(URL: string) {
        this.URL = URL;
    }
}

export default Connection;